import numpy
import cv2
import pygame
import socket
from threading import Thread

direction = numpy.zeros([1, 4], dtype=numpy.float32)
key_thread = True
control_thread = True


class KeyInputThread(Thread):

    def __init__(self):
        super(KeyInputThread, self).__init__()
        pygame.init()
        pygame.display.set_mode([300, 300])

    def run(self):
        global direction
        global key_thread
        global control_thread

        while key_thread:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("stop")
                    key_thread = False
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("stop")
                        key_thread = False
                        break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        direction[0][0] = 1
                    if event.key == pygame.K_RIGHT:
                        direction[0][1] = 1
                    if event.key == pygame.K_UP:
                        direction[0][2] = 1
                    if event.key == pygame.K_DOWN:
                        direction[0][3] = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        direction[0][0] = 0
                    if event.key == pygame.K_RIGHT:
                        direction[0][1] = 0
                    if event.key == pygame.K_UP:
                        direction[0][2] = 0
                    if event.key == pygame.K_DOWN:
                        direction[0][3] = 0

                print direction[0]

        control_thread = False


class CollectTrainingData(Thread):

    def __init__(self, host='localhost', port=8001):
        super(CollectTrainingData, self).__init__()
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.direction = numpy.zeros((1, 4), dtype=numpy.float32)
        self.conn = None
        self.client_address = None
        print self.direction

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print ("Listening for client . . .")
        self.conn, self.client_address = self.server_socket.accept()
        print ("Connected to client at ", self.client_address)
        self.conn.send("start")

    def receive_all(self, length):
        buf = b''
        while length:
            new_buf = self.conn.recv(length)
            if not new_buf:
                return None
            buf += new_buf
            length -= len(new_buf)
        return buf

    def get_frame(self, frame):

        # get the length of the data being sent
        length = self.receive_all(16)
        #print("Length of data = ", length)

        # Read data till length
        string_data = self.receive_all(int(length))
        #print("Data received")

        # convert to numpy array from string
        data = numpy.fromstring(string_data, dtype=numpy.uint8)

        # decode the recieved image
        decoded_img = cv2.imdecode(data, 0)

        print decoded_img.shape

        # save streamed images
        cv2.imwrite('../training_images/frame{:>05}.jpg'.format(frame), decoded_img)

    def run(self):
        global direction
        global control_thread

        # collect images for training
        print ('Start collecting images...')

        e1 = cv2.getTickCount()

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), dtype=numpy.float32)

        frame = 1

        while control_thread:
            self.conn.send("start")

            self.conn.send("next")

            self.get_frame(frame)

            self.conn.send(str(self.direction[0]).strip("[").strip("]"))
            print (self.direction[0])

            frame += 1

            label_array = numpy.vstack((label_array, self.direction[0]))

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
        print ('Total frame:', frame)

        self.close()

    def close(self):
        # close connection
        self.conn.send("stop")
        self.conn.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


ctd = CollectTrainingData('0.0.0.0', 8001)
k = KeyInputThread()

ctd.connect()

k.start()
ctd.start()

k.join()
ctd.join()
