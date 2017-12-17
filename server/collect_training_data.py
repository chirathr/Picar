import numpy
import cv2
import pygame
import socket
from multiprocessing import Process


class CollectTrainingData(Process):

    def __init__(self, host='localhost',motor_port=8000, video_port=8001):
        super(CollectTrainingData, self).__init__()
        self.video_address = (host, video_port)
        self.video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.motor_address = (host, motor_port)
        self.motor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.send_inst = True

        # pygame
        pygame.init()
        # pygame windows resolution 300x300
        pygame.display.set_mode([300, 300])

    def connect(self):
        self.video_server_socket.bind(self.video_address)
        self.video_server_socket.listen(5)
        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        print ("Connected to video client")

        self.motor_server_socket.bind(self.motor_address)
        self.motor_server_socket.listen(5)
        self.motor_connection = self.motor_server_socket.accept()
        print ("Connected to video client")

    def getDirection(self):
        pygame.event.pump()
        keyboard_state = pygame.key.get_pressed()
        self.direction[0][0] = keyboard_state[pygame.K_UP]
        self.direction[0][1] = keyboard_state[pygame.K_LEFT]
        self.direction[0][2] = keyboard_state[pygame.K_DOWN]
        self.direction[0][3] = keyboard_state[pygame.K_RIGHT]

    def run(self):
        self.direction = numpy.zeros([1, 4], dtype=numpy.float32)

        # collect images for training
        print ('Start collecting images...')

        e1 = cv2.getTickCount()

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), dtype=numpy.float32)

        frame = 1

        try:
            stream_bytes = ' '
            frame = 1
            while self.send_inst:
                stream_bytes += self.video_connection.read(1024)
                if stream_bytes.find('end') != -1:
                    self.send_inst = False
                    break
                first = stream_bytes.find('\xff\xd8')
                last = stream_bytes.find('\xff\xd9')
                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(numpy.fromstring(jpg, dtype=numpy.uint8), 0)

                    # select lower half of the image
                    roi = image[120:240, :]

                    # save streamed images
                    cv2.imwrite('../training_images/frame{:>05}.jpg'.format(frame), image)
                    self. getDirection()
                    print (self.direction[0])

                    self.motor_connection.send(str(self.direction[0]).strip("[").strip("]"))

                    frame += 1

                    label_array = numpy.vstack((label_array, self.direction[0]))

                    #cv2.imshow('roi_image', roi)
                    # cv2.imshow('image', image)

            # save training labels
            train_labels = label_array[1:, :]

            # save label data as a numpy file
            print("saving file")
            numpy.savez('../training_data/data000.npz', train_labels=train_labels)

            e2 = cv2.getTickCount()
            # calculate streaming duration
            time0 = (e2 - e1) / cv2.getTickFrequency()
            print ('Streaming duration:', time0)

            # print(train.shape)
            print(train_labels.shape)
            print ('fps:', frame/time0)

        finally:
            self.close()

    def close(self):
        # close connection
        self.motor_connection.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


ctd = CollectTrainingData('0.0.0.0', 8001)
ctd.connect()
ctd.start()
ctd.join()
