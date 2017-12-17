import socket
import sys
from ultrasonic import Ultrasonic
from multiprocessing import Process


class UltrasonicStreamClient(Process):
    def __init__(self, host="localhost", port=8001):
        super(UltrasonicStreamClient, self).__init__()
        self.address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ultrasonic = Ultrasonic()

    def connect(self):
        print("Connecting to server at ", self.address[0], " ", self.address[1])
        self.client_socket.connect(self.address)

    def run(self):
        data = self.client_socket.recv(2048)

        if data.strip() == "start":
            while True:
                data = self.client_socket.recv(2048)
                if data.strip() == "get-distance":
                    self.client_socket.send(str(self.ultrasonic.distance()).strip("[").strip("]"))

                if data.strip() == "stop":
                    self.close()

    def close(self):
        self.client_socket.close()
        self.ultrasonic.close()
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Error! usage: %s host-ip port" % __file__)
        sys.exit()
    ultrasonicStreamClient = UltrasonicStreamClient(sys.argv[1], int(sys.argv[2]))
    ultrasonicStreamClient.connect()
    ultrasonicStreamClient.start()
    ultrasonicStreamClient.join()
