import numpy
import cv2
import pygame
import socket
import sys
from multiprocessing import Process


class CollectTrainingData(Process):

    def __init__(self, host='localhost', motor_port=8000, video_port=8001):
        super(CollectTrainingData, self).__init__()

        # create two sockets
        self.video_address = (host, video_port)
        self.video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.motor_address = (host, motor_port)
        self.motor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.send_inst = True

        self.motor_connection = None
        self.video_connection = None

        # the car direction array
        self.direction = numpy.zeros([1, 4], dtype=numpy.float32)

        # initialise pygame window
        pygame.init()

        # set pygame windows resolution as 300x300
        pygame.display.set_mode([300, 300])

    def connect(self):
        # create a server for the motor stream
        self.motor_server_socket.bind(self.motor_address)
        self.motor_server_socket.listen(5)
        self.motor_connection = self.motor_server_socket.accept()
        print ("Connected to motor client")

        # server to get video stream from the car
        self.video_server_socket.bind(self.video_address)
        self.video_server_socket.listen(5)
        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        print ("Connected to video client")

    def get_direction(self):
        """get the current state of keyboard and save it to direction array"""
        pygame.event.pump()

        # get current keyboard state
        keyboard_state = pygame.key.get_pressed()

        # assign the keyboard states into the direction array
        self.direction[0][0] = keyboard_state[pygame.K_UP]
        self.direction[0][1] = keyboard_state[pygame.K_LEFT]
        self.direction[0][2] = keyboard_state[pygame.K_DOWN]
        self.direction[0][3] = keyboard_state[pygame.K_RIGHT]

    def run(self):
        self.connect()
        self.motor_connection.send('start')

        # collect images for training
        print ('Start collecting images...')

        e1 = cv2.getTickCount()

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), dtype=numpy.float32)

        try:
            stream_bytes = ' '
            frame = 1
            while True:
                stream_bytes += self.video_connection.read(1024)

                # stop saving data on seeing 'stop'
                if stream_bytes.find('stop') != -1:
                    break

                # fin the start and end of image in the binary data
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:

                    # get the image from the stream
                    jpg = stream_bytes[first:last + 2]

                    # increment the steam buffer
                    stream_bytes = stream_bytes[last + 2:]

                    # convert string to image data
                    image = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 0)

                    # select lower half of the image
                    # roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('../training_images/frame{:>05}.jpg'.format(frame), image)

                    # get input from the keyboard
                    self.get_direction()

                    print (self.direction[0])

                    # sent keyboard input to the motor controller
                    self.motor_connection.send(str(self.direction[0]).strip("[").strip("]"))

                    # add direction to the label array
                    label_array = numpy.vstack((label_array, self.direction[0]))

                    # display the image on screen
                    cv2.imshow('image', image)

                    frame += 1

            # save training labels
            train_labels = label_array[1:, :]

            # save label data as a numpy file
            numpy.savez('../training_data/data000.npz', train_labels=train_labels)
            print("labels saved to file training_data/data000.npz")

            e2 = cv2.getTickCount()

            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print ('Streaming duration:', time0)

            print(train_labels.shape)
            print ('fps:', frame / time0)

        finally:
            self.close()

    def close(self):
        # close connection
        self.motor_onnection.send("stop")
        self.motor_connection.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ("Error! usage: %s host-ip motor-port video-port" % __file__)
        sys.exit()
    ctd = CollectTrainingData(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]))
    ctd.start()
    ctd.join()
