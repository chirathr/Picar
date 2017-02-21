from connection.client import Client
from motor.motorControl import Motor


client = Client()
motor = Motor()

c = client.connect(12345)

while 1:
    print(c.recv(1024))


c.close()
