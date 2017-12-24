import socket
import sys
from multiprocessing import Process


class ClientSocket(Process):
    def __init__(self, host, port, name):
        super(ClientSocket, self).__init__()
        self.address = (host, port)
        self.name = name
        self.client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.client_sock.connect(self.address)
        print ("client %s connected to server %s" % (self.name, str(self.address)))

    def run(self):
        self.connect()
        for i in range(10):
            self.client_sock.send("ping %d, I am %s" % (i, self.name))

    def close(self):
        self.client_sock.close()
        sys.exit()


if __name__ == '__main__':
    cs1 = ClientSocket('localhost', 8000, '1')
    cs2 = ClientSocket('localhost', 8001, '2')
    cs3 = ClientSocket('localhost', 8002, '3')

    cs1.start()
    cs2.start()
    cs3.start()

    cs1.join()
    cs2.join()
    cs3.join()

