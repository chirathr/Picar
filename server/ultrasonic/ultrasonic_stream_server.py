import socket

class UltrasonicStreamServer(object):
    def __inti__(self, host="localhost", port=8002):
        self.address = (host, port)
		self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

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

uS = UltrasonicStreamServer('192.168.43.50', 8002)
us.connect()
print us.get()
us.close()
