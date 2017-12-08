import socket
import time
import sys
# import motor


class MotorController(object):
    def __init__(self, host='localhost', port=8000):
        self.address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.motor = Motor()

    def connect(self):
        print("Connectin to server at ", self.address[0], " ", self.address[1])
        self.client_socket.connect(self.address)

    def start(self):
        data = self.client_socket.recv(2048)

        if data.strip() == "start":
            while True:
                data = self.client_socket.recv(2048)
                direction = data.split(", ")
                print(direction)

                # code to run motor

                motor.drive(direction)

                if data.strip() == "dack":
                    self.close()

    def close(self):
        self.client_socket.close()
        sys.exit()


mC = MotorController("localhost", 8002)
mC.connect()
mC.start()
