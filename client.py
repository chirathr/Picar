from connection.client import Client

client = Client()

c = client.connect(12345)

while 1:
    print(c.recv(1024))

c.close()
