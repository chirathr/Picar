#!/usr/bin/python           # This is client.py file
import socket               # Import socket module

class Client(object):
    self.s = None
    self.host = None
    self.port = None

    def connect(self, port):
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname() # Get local machine name
        self.port = port                # Reserve a port for your service.
        self.s.connect((host, port))

        return self.s

    def close(self):
        self.s.close()
