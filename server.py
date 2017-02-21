from connection.server import SocketServer

ss = SocketServer()

ss.connect(5000)

ss.start_sending()

ss.close()
