import socket
import sys
from multiprocessing import Process


class ServerSocket(Process):
    def __init__(self, host, port, name):
        super(ServerSocket, self).__init__()
        self.address = (host, port)
        self.name = name
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.client_address = None

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        self.conn, self.client_address = self.server_socket.accept()
        print "Connected to client at ", self.client_address

    def run(self):
        self.connect()
        for i in range(10):
            print(self.conn.recv(1024).strip())

        self.conn.close()

    def close(self):
        self.server_socket.close()
        sys.exit()


if __name__ == '__main__':
    cs1 = ServerSocket('localhost', 8000, '1')
    cs2 = ServerSocket('localhost', 8001, '2')
    cs3 = ServerSocket('localhost', 8002, '3')

    cs1.start()
    cs2.start()
    cs3.start()

    cs1.join()
    cs2.join()
    cs3.join()
