
# import tkinter as tk
# from tkinter import scrolledtext, messagebox
# import socket
# import threading
# import ssl

# class IRCClient:
#     def __init__(self, nickname, realname):
#         self.nickname = nickname
#         self.realname = realname
#         self.socket = None
#         self.connected = False

#     def connect(self, host, port, ssl_enabled=False):
#         try:
#             self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#             if ssl_enabled:
#                 self.socket = ssl.wrap_socket(self.socket)
#             self.socket.connect((host, port))
#             self.send("USER {} 0 * :{}\r\n".format(self.nickname, self.realname))
#             self.send("NICK {}\r\n".format(self.nickname))
#             self.connected = True
#         except Exception as e:
#             messagebox.showerror("Error", "No se pudo conectar al otro cliente: {}".format(e))

#     def send(self, message):
#         if self.connected:
#             try:
#                 self.socket.sendall(message.encode("UTF-8"))
#             except Exception as e:
#                 messagebox.showerror("Error", "Error al enviar mensaje: {}".format(e))

#     def receive(self):
#         if self.connected:
#             try:
#                 while True:
#                     message = self.socket.recv(2048).decode("UTF-8")
#                     if message.startswith("PING"):
#                         self.send("PONG {}\r\n".format(message.split()[1]))
#                     print(message)
#             except Exception as e:
#                 messagebox.showerror("Error", "Error al recibir mensaje: {}".format(e))

# class IRCClientGUI:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Cliente IRC P2P")

#         # Campos de entrada para nickname, IP y puerto del otro cliente
#         self.nickname_label = tk.Label(root, text="Nickname:")
#         self.nickname_label.grid(row=0, column=0)
#         self.nickname_entry = tk.Entry(root)
#         self.nickname_entry.grid(row=0, column=1)

#         self.ip_label = tk.Label(root, text="IP del otro cliente:")
#         self.ip_label.grid(row=1, column=0)
#         self.ip_entry = tk.Entry(root)
#         self.ip_entry.grid(row=1, column=1)

#         self.port_label = tk.Label(root, text="Puerto del otro cliente:")
#         self.port_label.grid(row=2, column=0)
#         self.port_entry = tk.Entry(root)
#         self.port_entry.grid(row=2, column=1)

#         # Botones para conectar, desconectar, enviar mensajes
#         self.connect_button = tk.Button(root, text="Conectar", command=self.connect_to_peer)
#         self.connect_button.grid(row=3, column=0, columnspan=2)

#         self.disconnect_button = tk.Button(root, text="Desconectar", command=self.disconnect, state=tk.DISABLED)
#         self.disconnect_button.grid(row=4, column=0, columnspan=2)

#         self.message_label = tk.Label(root, text="Mensaje:")
#         self.message_label.grid(row=5, column=0)
#         self.message_entry = tk.Entry(root)
#         self.message_entry.grid(row=5, column=1)

#         self.send_button = tk.Button(root, text="Enviar", command=self.send_message, state=tk.DISABLED)
#         self.send_button.grid(row=6, column=0, columnspan=2)

#         # Área de texto para mostrar el chat
#         self.chat_text = scrolledtext.ScrolledText(root, width=40, height=10)
#         self.chat_text.grid(row=7, column=0, columnspan=2)

#         # Instancia del cliente IRC
#         self.irc_client = None

#     def connect_to_peer(self):
#         if not self.irc_client:
#             nickname = self.nickname_entry.get()
#             ip = self.ip_entry.get()
#             port = self.port_entry.get()
#             if nickname and ip and port:
#                 try:
#                     port = int(port)
#                     # Conectarse al otro cliente (sin SSL por defecto)
#                     self.irc_client = IRCClient(nickname, "Nombre Real")
#                     self.irc_client.connect(ip, port)
#                     self.irc_client_thread = threading.Thread(target=self.irc_client.receive)
#                     self.irc_client_thread.start()
#                     # Actualizar estado de los botones
#                     self.connect_button.config(state=tk.DISABLED)
#                     self.disconnect_button.config(state=tk.NORMAL)
#                     self.send_button.config(state=tk.NORMAL)
#                 except Exception as e:
#                     messagebox.showerror("Error", "No se pudo conectar al otro cliente: {}".format(e))
#             else:
#                 messagebox.showerror("Error", "Por favor, completa todos los campos.")

#     def disconnect(self):
#         if self.irc_client:
#             self.irc_client.connected = False
#             self.irc_client.socket.close()
#             # Actualizar estado de los botones
#             self.connect_button.config(state=tk.NORMAL)
#             self.disconnect_button.config(state=tk.DISABLED)
#             self.send_button.config(state=tk.DISABLED)

#     def send_message(self):
#         if self.irc_client:
#             message = self.message_entry.get()
#             if message:
#                 self.irc_client.send(message + "\r\n")
#                 self.message_entry.delete(0, tk.END)

# if __name__ == "__main__":
#     root = tk.Tk()
#     gui = IRCClientGUI(root)
#     root.mainloop()




import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
import ssl

class IRCClient:
    def __init__(self, server, port, nickname, realname, ssl_enabled=False):
        self.server = server
        self.port = port
        self.nickname = nickname
        self.realname = realname
        self.channel = None
        self.socket = None
        self.ssl_enabled = ssl_enabled
        self.connected = False

    def connect(self):
        try:
            server_ip = self.resolve_dns(self.server)
            if not server_ip:
                raise Exception("No se pudo resolver la dirección del servidor.")
            
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            if self.ssl_enabled:
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                self.socket = context.wrap_socket(self.socket, server_hostname=self.server)
            self.socket.connect((server_ip, self.port))
            self.send("USER {} 0 * :{}\r\n".format(self.nickname, self.realname))
            self.send("NICK {}\r\n".format(self.nickname))
            self.connected = True
        except Exception as e:
            messagebox.showerror("Error", "No se pudo conectar al servidor IRC: {}".format(e))

    def resolve_dns(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror as e:
            return None
        
        
    def disconnect(self):
        try:
            if self.socket:
                self.socket.close()
                self.connected = False
        except Exception as e:
            messagebox.showerror("Error", "Error al desconectar del servidor IRC: {}".format(e))

    def join_channel(self, channel):
        self.channel = channel
        self.send("JOIN {}\r\n".format(channel))

    def send_message(self, message):
        if self.channel:
            self.send("PRIVMSG {} :{}\r\n".format(self.channel, message))
        else:
            print("Not joined to any channel.")

    # Dentro del método receive_message en el cliente
    def receive_message(self):
        try:
            message = self.socket.recv(2048).decode("UTF-8")
            print("Received:", message)  # Agrega esta línea para verificar que se recibe el mensaje correctamente
            return message
        except Exception as e:
            messagebox.showerror("Error", "Error al recibir datos del servidor IRC: {}".format(e))
            return ""


    def send(self, message):
        self.socket.send(bytes(message, "UTF-8"))

    def handle_ping(self, message):
        if "PING" in message:
            self.send("PONG {}\r\n".format(message.split()[1]))

    def join_default_channel(self):
        if self.connected and self.channel:
            self.send("JOIN {}\r\n".format(self.channel))

    def run(self):
        self.connect()
        self.join_default_channel()  
        while self.connected:
            try:
                message = self.receive_message()
                print(message)
                self.handle_ping(message)
                self.display_message(message) 
            except Exception as e:
                print("Error:", e)
                break

    def display_message(self, message):
         self.text_area.insert(tk.END, message + "\n")


class IRCClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Cliente IRC")

        self.nickname_label = tk.Label(master, text="Nickname:")
        self.nickname_label.grid(row=0, column=0, sticky="w")

        self.nickname_entry = tk.Entry(master)
        self.nickname_entry.grid(row=0, column=1)

        self.server_label = tk.Label(master, text="Servidor:")
        self.server_label.grid(row=1, column=0, sticky="w")

        self.server_entry = tk.Entry(master)
        self.server_entry.grid(row=1, column=1)

        self.port_label = tk.Label(master, text="Puerto:")
        self.port_label.grid(row=2, column=0, sticky="w")

        self.port_entry = tk.Entry(master)
        self.port_entry.grid(row=2, column=1)
        self.port_entry.insert(0, "6667")

        self.ssl_var = tk.BooleanVar()
        self.ssl_checkbox = tk.Checkbutton(master, text="SSL", variable=self.ssl_var)
        self.ssl_checkbox.grid(row=3, column=0, columnspan=2)

        self.connect_button = tk.Button(master, text="Conectar", command=self.connect)
        self.connect_button.grid(row=4, column=0, columnspan=2)

        self.disconnect_button = tk.Button(master, text="Desconectar", command=self.disconnect, state=tk.DISABLED)
        self.disconnect_button.grid(row=5, column=0, columnspan=2)

        self.text_area = scrolledtext.ScrolledText(master, width=50, height=20)
        self.text_area.grid(row=6, columnspan=2)

        self.message_entry = tk.Entry(master, width=50)
        self.message_entry.grid(row=7, column=0, columnspan=2)

        self.send_button = tk.Button(master, text="Enviar", command=self.send_message, state=tk.DISABLED)
        self.send_button.grid(row=8, column=0, columnspan=2)

        self.irc_socket = None
        self.ssl_enabled = False
        self.connected = False
        self.nickname = None

    def connect(self):
        self.nickname = self.nickname_entry.get()
        server = self.server_entry.get()
        port = int(self.port_entry.get())
        self.ssl_enabled = self.ssl_var.get()

        try:
            server_ip = self.resolve_dns(server)
            if not server_ip:
                raise Exception("No se pudo resolver la dirección del servidor.")

            if self.ssl_enabled:
                context = ssl.create_default_context()
                self.irc_socket = context.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=server)
            else:
                self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            self.irc_socket.connect((server_ip, port))
            self.connected = True
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.send_button.config(state=tk.NORMAL)
            self.text_area.insert(tk.END, "Conectado al servidor IRC.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Error al conectar al servidor IRC: {e}\n")

    def disconnect(self):
        try:
            if self.irc_socket:
                self.irc_socket.close()
                self.connected = False
                self.connect_button.config(state=tk.NORMAL)
                self.disconnect_button.config(state=tk.DISABLED)
                self.send_button.config(state=tk.DISABLED)
                self.text_area.insert(tk.END, "Desconectado del servidor IRC.\n")
        except Exception as e:
            self.text_area.insert(tk.END, f"Error al desconectar del servidor IRC: {e}\n")

    def send_message(self):
        message = self.message_entry.get()
        if self.irc_socket and message:
            try:
                self.irc_socket.sendall(f"PRIVMSG {self.server_entry.get()} :{message}\r\n".encode("utf-8"))
                self.text_area.insert(tk.END, f"{self.nickname}: {message}\n")
                self.message_entry.delete(0, tk.END)
            except Exception as e:
                self.text_area.insert(tk.END, f"Error al enviar el mensaje: {e}\n")

    def resolve_dns(self, hostname):
        try:
            return socket.gethostbyname(hostname)
        except socket.gaierror:
            return None

root = tk.Tk()
app = IRCClientGUI(root)
root.mainloop()