import socket
import threading

class IRCClient:
    def __init__(self, host, port, nickname):
        self.host = host
        self.port = port
        self.nickname = nickname
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False

    def connect(self):
        try:
            self.socket.connect((self.host, self.port))
            self.connected = True
            self.socket.sendall(self.nickname.encode())
        except Exception as e:
            print("Error al conectar:", e)
            self.connected = False

    def send_message(self, message):
        try:
            self.socket.sendall(message.encode())
        except Exception as e:
            print("Error al enviar mensaje:", e)

    def receive_messages(self):
        while True:
            try:
                message = self.socket.recv(1024).decode()
                print(message)
            except Exception as e:
                print("Error al recibir mensaje:", e)
                break

def main():
    # Cambia 'localhost' por la dirección IP del servidor en la red local
    server_ip = input("Ingrese la dirección IP del servidor: ")
    nickname = input("Ingrese su apodo: ")
    irc_client = IRCClient(server_ip, 8888, nickname)
    irc_client.connect()

    if irc_client.connected:
        print(f"Bienvenido, {nickname}!\n")
        threading.Thread(target=irc_client.receive_messages, daemon=True).start()

        while True:
            message = input()
            irc_client.send_message(message)

            # Esperar a que se reciba la lista de canales
            if message == "/list":
                continue

    else:
        print("No se pudo conectar al servidor. Por favor, vuelva a intentarlo más tarde.")

if __name__ == "__main__":
    main()
