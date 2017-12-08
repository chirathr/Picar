import io
import socket
import struct
import time
import picamera


class VideoStream(object):
    def __init__(self, host="localhost", port=8001):
		self.address = (host, port)
		self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def connect(self):
		print("Connectin to server at ", self.address[0], " ", self.address[1])
        self.client_socket.connect(self.address)

    def start(self):
        while True:
            start_time = time.time()

            # read the image to be sent through the network
            img = cv2.imread('img_fjords.jpg', 0)

            # encoding parameters
            encode_param=[int(cv2.IMWRITE_JPEG_QUALITY), 90]

            # encoded value saved in imgEncode
            result, imgEncode = cv2.imencode('.jpg', img, encode_param)

            # convert to numpy array
            image_array = numpy.array(imgEncode)

            # convert numpy array to string
            string_data = image_array.tostring()

            # sent the lenght of the image string
            print("Lenght of data = ", len(string_data))
            self.client_socket.send( str(len(string_data)).ljust(16));

            # sent the data to the server
            self.client_socket.send( string_data )
            print("Data sent")

            self.client_socket.flush()

            if time.time() - start_time > 600:
                break

        self.close()



    # def start(self):
    #     try:
    #         with picamera.PiCamera() as camera:
    #             camera.resolution = (320, 240)      # pi camera resolution
    #             camera.framerate = 10               # 10 frames/sec
    #             time.sleep(2)                       # give 2 secs for camera to initilize
    #             start_time = time.time()
    #             stream = io.BytesIO()
    #
    #             # send jpeg format video stream
    #             for foo in camera.capture_continuous(stream, 'jpeg',
    #                                                  use_video_port = True):
    #                 # encoded value saved in imgEncode
    #                 result, imgEncode = cv2.imencode('.jpg', img, self.encode_param)
    #
    #                 # convert to numpy array
    #                 image_array = numpy.array(imgEncode)
    #
    #                 # convert numpy array to string
    #                 string_data = image_array.tostring()
    #
    #                 # sent the lenght of the image string
    #                 self.client_socket.send(str(len(string_data)).ljust(16));
    #
    #                 # sent the data to the server
    #                 self.client_socket.send(string_data)
    #
    #                 self.client_socket.flush()
    #
    #                 if time.time() - start_time > 600:
    #                     break
    #     finally:
    #         self.close()

    def close(self):
        self.client_socket.close()
        sys.exit()
