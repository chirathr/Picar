from connection.server import SocketServer

ss = SocketServer()

ss.connect(12345)

ss.start_sending()
