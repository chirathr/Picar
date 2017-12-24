import socket
import sys


class UltrasonicStreamServer(object):
    def __init__(self, host="localhost", port=8002):
        super(UltrasonicStreamServer, self).__init__()
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.client_address = None

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print "Listening for client . . ."
        self.conn, self.client_address = self.server_socket.accept()
        print "Connected to client at ", self.client_address
        self.conn.send("start")

    def get(self):
        self.conn.send("get-distance")
        data = self.conn.recv(2018).strip()

        # convert to a dict

        return data

    def close(self):
        self.conn.send("stop")
        self.conn.close()
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Usage: %s host port" % __file__)
        sys.exit()
    ultrasonicStreamServer = UltrasonicStreamServer(sys.argv[1], sys.argv[2])
    ultrasonicStreamServer.connect()
    print (ultrasonicStreamServer.get())
    ultrasonicStreamServer.close()
