import socket
import sys
from motor import Motor
from multiprocessing import Process


class MotorController(Process):
    def __init__(self, host='localhost', port=8000):
        super(MotorController, self).__init__()
        self.address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.motor = Motor()

    def connect(self):
        print("Connectin to server at ", self.address[0], " ", self.address[1])
        self.client_socket.connect(self.address)

    def run(self):
        self.connect()
        data = self.client_socket.recv(2048)

        if data.strip() == "start":
            while True:
                data = self.client_socket.recv(2048)
                direction = data.split(", ")
                print(direction)

                # code to run motor

                self.motor.drive(direction)

                if data.strip() == "stop":
                    self.close()

    def close(self):
        self.motor.close()
        self.client_socket.close()
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Error! usage: %s host-ip port" % __file__)
        sys.exit()
    motorController = MotorController(sys.argv[1], int(sys.argv[2]))
    motorController.start()
    motorController.join()
