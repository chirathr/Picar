import pygame
import socket
import sys


class MotorControl(object):
    def __init__(self, host='localhost', port=8000):
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.direction = [0, 0, 0, 0]

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print "Listening for client . . ."
        self.conn, self.client_address = self.server_socket.accept()
        print "Connected to client at ", self.client_address

    def close(self):
        self.conn.send("dack")
        self.conn.close()
        sys.exit()

    def start(self):
        # self.conn.send("start")

        pygame.init()
        pygame.display.set_mode([300, 300])

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.close()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.direction[0] = 1
                    if event.key == pygame.K_LEFT:
                        self.direction[1] = 1
                    if event.key == pygame.K_DOWN:
                        self.direction[2] = 1
                    if event.key == pygame.K_RIGHT:
                        self.direction[3] = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        self.direction[0] = 0
                    if event.key == pygame.K_LEFT:
                        self.direction[1] = 0
                    if event.key == pygame.K_DOWN:
                        self.direction[2] = 0
                    if event.key == pygame.K_RIGHT:
                        self.direction[3] = 0
                self.conn.send(str(self.direction[0]) + ',' + str(self.direction[3]) + ',' +
                               str(self.direction[2]) + ',' + str(self.direction[1]))


mC = MotorControl('0.0.0.0', 8000)
mC.connect()
mC.start()
