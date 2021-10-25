import socket

from crypto_utility import Aes


class Secrets:

    @staticmethod
    def k1():
        return "first_key_______"

    @staticmethod
    def k2():
        return "second_key______"

    @staticmethod
    def k3():
        return "third_key_______"


class Server(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        print(f"INFO:\t server setup completed")
        self.first_node = None
        self.second_node = None
        self.encrypt_mode = ''

    def listen(self):
        self.socket.listen(2)
        self.first_node = self.socket.accept()[0]
        print(f"INFO:\t first node is connected")
        self.second_node = self.socket.accept()[0]
        print(f"INFO:\t second node is connected")

    def run(self):
        self.init_nodes_communication()
        while True:
            self.handle_comm_requests()

    def init_nodes_communication(self):
        self.set_encryption_type()
        self.provide_keys_to_nodes()

    def set_encryption_type(self):
        encryption_type = self.first_node.recv(3)
        print(f"INFO:\t first node wants to encrypt using { encryption_type.decode('UTF-8') }")
        self.second_node.send(encryption_type)
        print(f"INFO:\t second node was notifies to use { encryption_type.decode('UTF-8') } encryption mode")

    def provide_keys_to_nodes(self):
        key = Aes.encrypt(Secrets.k1(), Secrets.k3())
        if self.encrypt_mode == "cbc":
            key = Aes.encrypt(Secrets.k2(), Secrets.k3())
        self.first_node.send(key.encode('UTF-8'))
        self.second_node.send(key.encode('UTF-8'))
        print(f"INFO:\t nodes were notified to use '{ key }' key [encrypted]")

    def handle_comm_requests(self):
        first_node_msg = self.first_node.recv(1024)
        self.second_node.send(first_node_msg)
        print(f"INFO:\t first node sent to second one:'{ first_node_msg }'[encrypted]")
        second_node_msg = self.second_node.recv(1024)
        self.first_node.send(second_node_msg)
        print(f"INFO:\t second node sent to first one:'{ second_node_msg }'[encrypted]")


if __name__ == "__main__":
    HOST = 'localhost'
    PORT = 8009
    server = Server(HOST, PORT)
    server.listen()
    server.run()
