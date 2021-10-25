import socket
from crypto_utility import Aes


class Secrets:

    @staticmethod
    def k3():
        return "third_key_______"

    @staticmethod
    def init_vector():
        return "init_vector______"


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setblocking(True)
        self.encrypt_mode = 'CBC'
        self.key = ''

    def connect_to_server(self):
        self.socket.connect((self.host, self.port))
        print(f"INFO:\t client successfully completed to server")

    def setup_communication(self):
        self.encrypt_mode = self.socket.recv(3).decode("UTF-8")
        print(f"INFO:\t Confirmation, I will use { self.encrypt_mode } encryption mode")
        self.key = self.socket.recv(32)
        self.key = self.key.decode("UTF-8")
        print(f"INFO:\t Confirmation, I will use '{self.key}' encryption key [encrypted]")
        self.key = Aes.decrypt(self.key, Secrets.k3())
        print(f"INFO:\t Actual key '{self.key}' encryption key [decrypted]")

    def communicate(self):
        while True:
            self.receive_msg()
            self.send_msg()

    def receive_msg(self):
        encrypted_msg = self.socket.recv(1024)
        msg = self.decrypt_msg(encrypted_msg.decode("UTF-8"))
        print(f"INFO:\t Second node said: '{msg}' [decrypted]")

    def send_msg(self):
        answer = input(" MSG:\t ")
        print(f"INFO:\t Sending message to first node: '{answer}' [decrypted]")
        encrypted_answer = self.encrypt_msg(answer)
        self.socket.sendall(encrypted_answer.encode("UTF-8"))

    def encrypt_msg(self, msg):
        if self.encrypt_mode == "CBC":
            return Aes.cbc_encrypt(msg, Secrets.init_vector(), Secrets.k3())
        return Aes.ecb_encrypt(msg, Secrets.k3())

    def decrypt_msg(self, msg):
        if self.encrypt_mode == "CBC":
            return Aes.cbc_decrypt(msg, Secrets.init_vector(), Secrets.k3())
        return Aes.ecb_decrypt(msg, Secrets.k3())


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8009
    client = Client(HOST, PORT)
    client.connect_to_server()
    client.setup_communication()
    client.communicate()
