import numpy
import cv2
import pygame
import socket
from multiprocessing import Process

direction = numpy.zeros([1, 4], dtype=numpy.float32)
key_thread = True
control_thread = True
send_inst = True

class KeyInputThread(Process):
    """
    The class creates a window to input direction from keyboard. Inputs include left, right, up and down arrow keys.
    The direction list is a static global variable that can be accessed from another thread. Esc to quit.
    """

    def __init__(self):
        """
        Initialise pygame window
        """
        super(KeyInputThread, self).__init__()
        pygame.init()
        # pygame windows resolution 300x300
        pygame.display.set_mode([300, 300])

    def run(self):
        """
        collects the current keyboard input and stored in global variable direction
        :return:
        """
        global direction
        global key_thread
        global control_thread
        global send_inst

        while key_thread:

            for event in pygame.event.get():
                # quit when close button or esc key is pressed.
                if event.type == pygame.QUIT:
                    print("stop")
                    key_thread = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("stop")
                        key_thread = False
                        break

                # set direction = 1 on key press [up, left, down, right]
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        direction[0][0] = 1
                    if event.key == pygame.K_LEFT:
                        direction[0][1] = 1
                    if event.key == pygame.K_DOWN:
                        direction[0][2] = 1
                    if event.key == pygame.K_RIGHT:
                        direction[0][3] = 1

                # set direction = 0 on key up
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        direction[0][0] = 0
                    if event.key == pygame.K_LEFT:
                        direction[0][1] = 0
                    if event.key == pygame.K_DOWN:
                        direction[0][2] = 0
                    if event.key == pygame.K_RIGHT:
                        direction[0][3] = 0

        # exit the collect training data thread3
        control_thread = False
        send_inst = False


class CollectTrainingData(Process):

    def __init__(self, host='localhost', port=8001):
        super(CollectTrainingData, self).__init__()
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.client_address = None
        self.send_inst = True

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print ("Listening for client . . .")
        self.conn = self.server_socket.accept()[0].makefile('rb')

    def run(self):
        global direction
        global control_thread
        global send_inst

        # collect images for training
        print ('Start collecting images...')

        e1 = cv2.getTickCount()

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), dtype=numpy.float32)

        frame = 1

        try:
            stream_bytes = ' '
            frame = 1
            while send_inst:
                if frame > 700:
                    break
                stream_bytes += self.conn.read(1024)
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

                    print (direction[0])

                    frame += 1

                    label_array = numpy.vstack((label_array, direction[0]))

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
        # self.conn.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


ctd = CollectTrainingData('localhost', 8001)
k = KeyInputThread()

ctd.connect()

k.start()
ctd.start()

k.join()
ctd.join()
