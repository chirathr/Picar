import socket
import cv2
import numpy
import time

# host and port
host='localhost'
port=8000
address = (host, port)

# create a server that listens for a single client
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(address)
print("Server started, waiting for client")
server_socket.listen(5)
conn, client_address = server_socket.accept()

# function to get all the bytes till count
def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf
start_time = time.time()
while True:
    # get the length of the data being sent
    conn.send("next")
    length = recvall(conn, 16)
    print("Lenght of data = ", length)

    # Read data till length
    stringData = recvall(conn, int(length))
    print("Data recieved")

    # convert to numpy array from string
    data = numpy.fromstring(stringData, dtype='uint8')

    # display the recieved image
    print("Image displayed, press any key to exit.")
    decimg=cv2.imdecode(data,1)
    cv2.imshow('SERVER', decimg)

    if time.time() - start_time > 10:
        # close connection
        conn.close()
        server_socket.close()
        break

# wait for a key and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
