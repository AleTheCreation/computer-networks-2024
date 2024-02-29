import socket
import threading

class CentralServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def handle_client(self, client_socket):
        while True:
            try:
                message = client_socket.recv(1024)
                if not message:
                    break
                self.broadcast(message, client_socket)
            except Exception as e:
                print("Error:", e)
                break

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message)
                except Exception as e:
                    print("Error al enviar mensaje:", e)

    def start(self):
        print("Servidor centralizado iniciado.")
        while True:
            client_socket, _ = self.server_socket.accept()
            self.clients.append(client_socket)
            threading.Thread(target=self.handle_client, args=(client_socket,), daemon=True).start()

class IRCServer:
    def __init__(self, host, port, central_server_host, central_server_port):
        self.host = host
        self.port = port
        self.central_server_host = central_server_host
        self.central_server_port = central_server_port
        self.clients = {}
        self.channels = {"general": []}  # Agregamos el canal "general" por defecto

    def handle_client(self, client_socket, client_address):
        nickname = client_socket.recv(1024).decode("utf-8")
        self.clients[nickname] = client_socket
        print(f"{nickname} se ha unido al servidor.")
        self.send_message_to_all(f"{nickname} se ha unido al servidor.")
        while True:
            try:
                message = client_socket.recv(1024).decode("utf-8")
                if message:
                    if message.startswith("/join"):
                        channel = message.split()[1]
                        self.join_channel(nickname, channel)
                    elif message.startswith("/create"):
                        channel = message.split()[1]
                        self.create_channel(channel)
                        self.join_channel(nickname, channel)
                    elif message.startswith("/list"):
                        self.list_channels(client_socket)
                    elif message.startswith("/msg"):
                        recipient, msg_content = message.split(maxsplit=2)[1:]
                        self.send_private_message(nickname, recipient, msg_content)
                    elif message.startswith("/quit"):
                        self.quit_server(nickname)
                        break
                    else:
                        self.send_message_to_channel(f"{nickname}: {message}", "general")
            except Exception as e:
                print(e)
                break

    def join_channel(self, nickname, channel):
        if channel not in self.channels:
            self.channels[channel] = []
        self.channels[channel].append(nickname)
        self.send_message_to_channel(f"{nickname} se ha unido al canal {channel}.", channel)

    def create_channel(self, channel):
        if channel not in self.channels:
            self.channels[channel] = []

    def quit_server(self, nickname):
        del self.clients[nickname]
        self.send_message_to_all(f"{nickname} ha abandonado el servidor.")

    def send_message_to_all(self, message):
        for client_socket in self.clients.values():
            try:
                client_socket.sendall(message.encode("utf-8"))
            except:
                pass

    def send_message_to_channel(self, message, channel):
        if channel in self.channels:
            for member in self.channels[channel]:
                try:
                    self.clients[member].sendall(message.encode("utf-8"))
                except:
                    pass

    def send_private_message(self, sender, recipient, message):
        if recipient in self.clients:
            try:
                self.clients[recipient].sendall(f"Mensaje privado de {sender}: {message}".encode("utf-8"))
            except:
                pass

    def list_channels(self, client_socket):
        channels_str = ", ".join(self.channels.keys())
        client_socket.sendall(f"Canales disponibles: {channels_str}\n".encode("utf-8"))


    def start(self):
        print(f"Servidor IRC iniciado en {self.host}:{self.port}")
        central_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        central_server_socket.connect((self.central_server_host, self.central_server_port))
        central_server_socket.sendall("Connected".encode("utf-8"))

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)

        while True:
            client_socket, client_address = self.server_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    central_server = CentralServer("localhost", 8888)
    irc_server = IRCServer("localhost", 6667, "localhost", 8888)
    
    central_server_thread = threading.Thread(target=central_server.start)
    irc_server_thread = threading.Thread(target=irc_server.start)
    
    central_server_thread.start()
    irc_server_thread.start()
