import numpy
import cv2
import pygame
import socket


class CollectTrainingData(object):

    def __init__(self, host='localhost', port=8001):
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.direction = numpy.zeros((1, 4), dtype = numpy.float32)
        print self.direction

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print ("Listening for client . . .")
        self.conn, self.client_address = self.server_socket.accept()
        print ("Connected to client at ", self.client_address)
        self.conn.send("start")

    def recvall(self, sock, length):
        buf = b''
        while length:
            newbuf = sock.recv(length)
            if not newbuf:
                return None
            buf += newbuf
            length -= len(newbuf)
        return buf

    def get_frame(self, frame):

        # get the length of the data being sent
        length = self.recvall(self.conn, 16)
        print("Lenght of data = ", length)

        # Read data till length
        stringData = self.recvall(self.conn, int(length))
        print("Data recieved")

        # convert to numpy array from string
        data = numpy.fromstring(stringData, dtype=numpy.uint8)

        # decode the recieved image
        decimg = cv2.imdecode(data, 0)

        print decimg.shape

        # save streamed images
        cv2.imwrite('../training_images/frame{:>05}.jpg'.format(frame), decimg)

        #cv2.imshow('roi_image', roi)

        #cv2.imshow('image', decimg)
        #cv2.waitKey(25)


    def start(self):

        pygame.init()
        pygame.display.set_mode([300,300])

        # collect images for training
        print ('Start collecting images...')

        e1 = cv2.getTickCount()

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), dtype = numpy.float32)

        frame = 1
        self.conn.send("start")

        temp = numpy.zeros((1, 4), dtype = numpy.float32)

        temp = self.direction[:]

        flag = 1

        while True:

            if (flag == 0):
                break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("stop")
                    flag = 0
                    break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        print("stop")
                        flag = 0
                        break

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.direction[0][0] = 1
                    if event.key == pygame.K_RIGHT:
                        self.direction[0][1] = 1
                    if event.key == pygame.K_UP:
                        self.direction[0][2] = 1
                    if event.key == pygame.K_DOWN:
                        self.direction[0][3] = 1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        self.direction[0][0] = 0
                    if event.key == pygame.K_RIGHT:
                        self.direction[0][1] = 0
                    if event.key == pygame.K_UP:
                        self.direction[0][2] = 0
                    if event.key == pygame.K_DOWN:
                        self.direction[0][3] = 0


                self.conn.send(str(self.direction).strip("[").strip("]"))
                print (self.direction)
                self.conn.send("next")

                self.get_frame(frame)

                frame += 1

               # image_array = numpy.vstack((image_array, temp_array))
                label_array = numpy.vstack((label_array, self.direction))

                temp = self.direction[:]

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
ctd.connect()
ctd.start()
