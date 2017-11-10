"""
Reference:
PiCamera documentation
https://picamera.readthedocs.org/en/release-1.10/recipes2.html

"""

import io
import socket
import struct
import time
import picamera


class VideoStream(object):
    """
    Connect to server and stream camera feed
    """
    def __init__(self, ip_address, port_number):
        """create socket and bind host"""
        self.connect()

    def connect(self, ip_address, port_number):
        """
        Connect to the given ip address and port number
        """
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip_address, port_number))
        self.connection = self.client_socket.makefile('wb')

    def stream_camera_feed(self):
        try:
            with picamera.PiCamera() as camera:
                camera.resolution = (320, 240)      # pi camera resolution
                camera.framerate = 10               # 10 frames/sec
                time.sleep(2)                       # give 2 secs for camera to initilize
                start = time.time()
                stream = io.BytesIO()

                # send jpeg format video stream
                for foo in camera.capture_continuous(stream, 'jpeg',
                                                     use_video_port = True):
                    connection.write(struct.pack('<L', stream.tell()))
                    connection.flush()
                    stream.seek(0)
                    connection.write(stream.read())
                    if time.time() - start > 600:
                        break
                    stream.seek(0)
                    stream.truncate()
            connection.write(struct.pack('<L', 0))
        finally:
            connection.close()
            client_socket.close()

    def close(self):
        connection.close()
        client_socket.close()
