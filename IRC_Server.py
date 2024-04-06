import socket
import threading

class IRCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connections = []
        self.channels = {"General": []}

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print(f"Servidor IRC iniciado en {self.host}:{self.port}")

        while True:
            client_socket, client_address = self.socket.accept()
            print(f"Nueva conexión desde {client_address}")
            client_handler = threading.Thread(target=self.handle_client, args=(client_socket,))
            client_handler.daemon = True
            client_handler.start()

    def handle_client(self, client_socket):
        self.connections.append(client_socket)
        client_socket.sendall("¡Bienvenido al servidor IRC local!\r\n".encode())

        self.join_channel(client_socket, "General")

        while True:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                message = data.decode().strip()
                print(f"Mensaje recibido: {message}")

                # Procesamiento de comandos
                if message.startswith("JOIN"):
                    channel = message.split(" ")[1]
                    self.join_channel(client_socket, channel)
                elif message.startswith("PART"):
                    channel = message.split(" ")[1]
                    self.leave_channel(client_socket, channel)
                elif message.startswith("MSG"):
                    parts = message.split(" ", 2)
                    if len(parts) >= 3:
                        target = parts[1]
                        msg = parts[2]
                        self.send_message(client_socket, target, msg)
                    else:
                        client_socket.sendall("Formato incorrecto. Uso: MSG <destino> <mensaje>\r\n".encode())
                elif message.startswith("NOTICE"):
                    parts = message.split(" ", 2)
                    if len(parts) >= 3:
                        target = parts[1]
                        notice = parts[2]
                        self.send_notice(client_socket, target, notice)
                    else:
                        client_socket.sendall("Formato incorrecto. Uso: NOTICE <destino> <mensaje>\r\n".encode())
                elif message.startswith("LIST"):
                    self.list_channels(client_socket)
                elif message.startswith("NAMES"):
                  parts = message.split(" ", 1)
                  if len(parts) > 1:
                      channel = parts[1]
                      self.list_users_in_channel(client_socket, channel)
                  else:
                      self.list_users_in_channel(client_socket, "General")

                elif message.startswith("NICK"):
                  parts = message.split(" ", 1)
                  if len(parts) > 1:
                     new_nickname = parts[1]
                     self.change_nickname(client_socket, new_nickname)
                  else:
                     client_socket.sendall("Formato incorrecto. Uso: NICK <nuevo_apodo>\r\n".encode())

                else:
                    self.send_message(client_socket, "General", message)

            except Exception as e:
                print(f"Error al manejar cliente: {e}")
                break

        client_socket.close()
        self.connections.remove(client_socket)
        print("Cliente desconectado")

    def list_channels(self, client_socket):
       client_socket.sendall("Lista de canales:\r\n".encode())
       for channel, users in self.channels.items():
         user_count = len(users)
         client_socket.sendall(f"- {channel} ({user_count} usuarios)\r\n".encode())
    
    def list_users_in_channel(self, client_socket, channel):
     if channel in self.channels:
        users = ', '.join([str(user_socket.getpeername()) for user_socket in self.channels[channel]])
        client_socket.sendall(f"Usuarios en el canal {channel}: {users}\r\n".encode())
     else:
        client_socket.sendall(f"No se encontró el canal {channel}\r\n".encode())


    def join_channel(self, client_socket, channel):
        self.channels[channel].append(client_socket)
        client_socket.sendall(f"Te has unido al canal {channel}\r\n".encode())

    def leave_channel(self, client_socket, channel):
        self.channels[channel].remove(client_socket)
        client_socket.sendall(f"Has dejado el canal {channel}\r\n".encode())

    def send_message(self, sender_socket, target, message):
        for channel in self.channels:
            if target == channel:
                for client_socket in self.channels[channel]:
                    if client_socket != sender_socket:
                        client_socket.sendall(f"Mensaje de {sender_socket.getpeername()}: {message}\r\n".encode())
                break
        else:
            sender_socket.sendall(f"No se encontró el canal {target}\r\n".encode())

    def send_notice(self, sender_socket, target, notice):
        for channel in self.channels:
            if target == channel:
                for client_socket in self.channels[channel]:
                    if client_socket != sender_socket:
                        client_socket.sendall(f"Notificación de {sender_socket.getpeername()}: {notice}\r\n".encode())
                break
        else:
            sender_socket.sendall(f"No se encontró el canal {target}\r\n".encode())

    def set_channel_mode(self, sender_socket, channel, mode):
        # Implementa la lógica para cambiar el modo de canal
        sender_socket.sendall(f"Modo del canal {channel} cambiado a {mode}\r\n".encode())

    def list_channels(self, client_socket):
        client_socket.sendall("Lista de canales:\r\n".encode())
        for channel in self.channels:
            client_socket.sendall(f"- {channel}\r\n".encode())

    def list_users_in_channel(self, client_socket, channel):
        for ch, users in self.channels.items():
            if ch == channel:
                client_socket.sendall(f"Usuarios en el canal {channel}:\r\n".encode())
                for user_socket in users:
                    client_socket.sendall(f"- {user_socket.getpeername()}\r\n".encode())
                break
        else:
            client_socket.sendall(f"No se encontró el canal {channel}\r\n".encode())

    def change_nickname(self, client_socket, new_nickname):
        # Implementa la lógica para cambiar el nickname del usuario
        pass

    def whois_query(self, client_socket, nickname):
        # Implementa la lógica para la consulta WHOIS
        pass

def main():
    server_ip = "127.0.0.1"
    port = 6667
    irc_server = IRCServer(server_ip, port)
    irc_server.start()

if __name__ == "__main__":
    main()
