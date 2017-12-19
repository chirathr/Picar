import socket


class ClientSocket(object):
    def __inti__(self):
        self.client_sock = socket.socket()