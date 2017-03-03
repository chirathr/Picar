#!/usr/bin/python           # This is client.py file
import socket               # Import socket module

class Client(object):
    s = None
    host = None
    port = None

    def connect(self, addr, port):
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = port                # Reserve a port for your service.
        self.s.connect((addr, port))

        return self.s

    def close(self):
        self.s.close()
