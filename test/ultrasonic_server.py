import socket
import time

class Sensor(object):
    def __init__(self, host='localhost', port=8000):
        self.server_socket = socket.socket()
        self.server_socket.bind(('192.168.1.100', 8002))
        self.server_socket.Listen(0)
        self.connection, self.client_address = self.server_socket.accept()
        self.streaming()

    def streaming(self):

        try:
            print "Connection from: ", self.client_address
            start = time.time()

            while True:
                sensor_data = str(self.connection.recv(1024))
                sensor_data = sensor_data.split(',')

                print "Distance: %0.1f cm" % sensor_data[0]
                print "Distance: %0.1f cm" % sensor_data[1]
                print "Distance: %0.1f cm" % sensor_data[2]
                print "Distance: %0.1f cm" % sensor_data[3]

                    # testing for 10 seconds
                if time.time() - start > 10:
                    break
        finally:
            self.connection.close()
            self.server_socket.close()

if __name__ == '__main__':
    Sensor()
