from connection.client import Client
from motor.motorControl import Motor


client = Client()
motor = Motor()

c = client.connect(5000)

while 1:
    key = c.recv(1024)
    print(key)
    motor.input(key)


c.close()
