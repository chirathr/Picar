import socket
import cv2
import numpy

host='localhost'
port=8000
address = (host, port)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(address)

img = cv2.imread('img_fjords.jpg', 0)


encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]


result, imgencode = cv2.imencode('.jpg', img, encode_param)

image_array = numpy.array(imgencode)


string_data = image_array.tostring()


client_socket.send( str(len(string_data)).ljust(16));
client_socket.send( string_data );

# close the socket connection
client_socket.close()
