import io
import sys
import socket
import struct
import time
import picamera
from multiprocessing import Process


class VideoStream(Process):
    def __init__(self, host='localhost', port=8001):
        super(VideoStream, self).__init__()
        self.address = (host, port)
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection = None

    def connect(self):
        print("Connecting to server to server at ", self.address[0], " ", self.address[1])
        self.client_socket.connect(self.address)
        self.connection = self.client_socket.makefile('wb')

    def run(self):
        self.connect()
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)      # pi camera resolution
                camera.framerate = 12               # 12 frames/sec
                time.sleep(2)                       # give 2 secs for camera to initialize
                start = time.time()
                stream = io.BytesIO()

                # send jpeg format video stream
                for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                    self.connection.write(struct.pack('<L', stream.tell()))
                    self.connection.flush()
                    print("frame sent")
                    stream.seek(0)
                    self.connection.write(stream.read())
                    if time.time() - start > 60:
                        break
                    stream.seek(0)
                    stream.truncate()
        finally:
            self.connection.write('stop')
            self.connection.flush()
            self.close()

    def close(self):
        self.client_socket.close()
        self.connection.close()
        sys.exit()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Error! usage: %s host-ip port" % __file__)
        sys.exit()
    videoStream = VideoStream(sys.argv[1], sys.argv[2])
    videoStream.start()
    videoStream.join()
