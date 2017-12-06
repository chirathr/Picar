import pygame
import sys
import socket
import sys

host = 'localhost'
port = 8223
address = (host, port)

direction = [0, 0, 0, 0]

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
server_socket.listen(5)

print "Listening for client . . ."
conn, address = server_socket.accept()
print "Connected to client at ", address

# pick a large output buffer size because i dont necessarily know how big the incoming packet is

conn.send("start")

pygame.init()
pygame.display.set_mode([100,100])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            conn.send("dack")
            conn.close()
            sys.exit() # if sys is imported

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                conn.send("dack")
                conn.close()
                sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                direction[0] = 1
            if event.key == pygame.K_RIGHT:
                direction[1] = 1
            if event.key == pygame.K_UP:
                direction[2] = 1
            if event.key == pygame.K_DOWN:
                direction[3] = 1

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                direction[0] = 0
            if event.key == pygame.K_RIGHT:
                direction[1] = 0
            if event.key == pygame.K_UP:
                direction[2] = 0
            if event.key == pygame.K_DOWN:
                direction[3] = 0
        conn.send(str(direction).strip("[").strip("]"))
