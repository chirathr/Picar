import socket
import time
import sys

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8002))

data = client_socket.recv(2048)

if data.strip() == "start":
    while True:
        data = client_socket.recv(2048)
        direction = data.split(", ")
        print(direction)

        if data.strip() == "dack":
            client_socket.close()
            sys.exit()

#send disconnect message
dmsg = "disconnect"
print "Disconnecting"
client_socket.send(dmsg)

client_socket.close()
