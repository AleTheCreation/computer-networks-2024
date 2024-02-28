import socket
import threading

class IRCServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((host, port))
        self.socket.listen(5)
        self.clients = {}
        self.channels = {}

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
                        if channel not in self.channels:
                            self.channels[channel] = []
                        self.channels[channel].append(nickname)
                        self.send_message_to_channel(f"{nickname} se ha unido al canal {channel}.", channel)
                    elif message.startswith("/msg"):
                        recipient, msg_content = message.split(maxsplit=2)[1:]
                        self.send_private_message(nickname, recipient, msg_content)
                    elif message.startswith("/quit"):
                        del self.clients[nickname]
                        self.send_message_to_all(f"{nickname} ha abandonado el servidor.")
                        break
                    else:
                        self.send_message_to_channel(f"{nickname}: {message}", "general")
            except Exception as e:
                print(e)
                break

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

    def start(self):
        print(f"Servidor IRC iniciado en {self.host}:{self.port}")
        while True:
            client_socket, client_address = self.socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

if __name__ == "__main__":
    server = IRCServer("localhost", 6667)
    server.start()
