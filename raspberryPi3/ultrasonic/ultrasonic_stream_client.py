# import ultrasonic
import socket

class UltrasonicStreamClient(object):
	def __init__(self, host="localhost", port=8001):
		self.address = (host, port)
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.ultrasonic = Ultrasonic()

	def connect(self):
		print("Connectin to server at ", self.ip, " ", self.port)
        self.client_socket.connect(self.address)

    def start(self):
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

uS = UltrasonicStreamClient('192.168.43.50', 8001)
us.connect()
us.start()
