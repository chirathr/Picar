import numpy
import cv2
import pygame
import socket


class CollectTrainingData(object):

    def __init__(self, host='localhost', port=8001):
        self.address = (host, port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.direction = [0, 0, 0, 0]

    def connect(self):
        self.server_socket.bind(self.address)
        self.server_socket.listen(5)
        print "Listening for client . . ."
        self.conn, self.client_address = self.server_socket.accept()
        print "Connected to client at ", self.client_address
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

    def start(self):
        saved_frame = 0
        total_frame = 0

        # collect images for training
        print 'Start collecting images...'

        e1 = cv2.getTickCount()

        # 320 * 120
        image_array = numpy.zeros((1, 38400))

        # [front, right, reverse, left]
        label_array = numpy.zeros((1, 4), 'float')

        # create labels
        self.k = numpy.zeros((4, 4), 'float')
        for i in range(4):
            self.k[i, i] = 1
        self.temp_label = numpy.zeros((1, 4), 'float')

        frame = 1

        self.conn.send("start")

        while True:
            # get the length of the data being sent
            length = self.recvall(self.conn, 16)
            print("Lenght of data = ", length)

            # Read data till length
            stringData = self.recvall(self.conn, int(length))
            print("Data recieved")

            # convert to numpy array from string
            data = numpy.fromstring(stringData, dtype=numpy.uint8)

            # display the recieved image
            decimg=cv2.imdecode(data, 0)

            # save streamed images
            cv2.imwrite('../training_images/frame{:>05}.jpg'.format(frame), decimg)

            #cv2.imshow('roi_image', roi)
            cv2.imshow('image', decimg)

            # select lower half of the image
            roi = decimg[120:240, :]

            print roi.shape

            # reshape the roi image into one row array
            temp_array = roi.reshape(1, 38400).astype(numpy.float32)

            frame += 1
            total_frame += 1

            # get input from human driver
            event = pygame.event.poll()
            if event.type == pygame.QUIT:
                self.close()
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.close()
                    break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction[0] = 1
                if event.key == pygame.K_RIGHT:
                    self.direction[1] = 1
                if event.key == pygame.K_UP:
                    self.direction[2] = 1
                if event.key == pygame.K_DOWN:
                    self.direction[3] = 1

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.direction[0] = 0
                if event.key == pygame.K_RIGHT:
                    self.direction[1] = 0
                if event.key == pygame.K_UP:
                    self.direction[2] = 0
                if event.key == pygame.K_DOWN:
                    self.direction[3] = 0

            self.conn.send(str(self.direction).strip("[").strip("]"))

            image_array = numpy.vstack((image_array, temp_array))
            label_array = numpy.vstack((label_array, direction))
            saved_frame += 1

            print direction

            self.conn.send("next")

        # save training images and labels
        train = image_array[1:, :]
        train_labels = label_array[1:, :]

        # save training data as a numpy file
        numpy.savez('training_data_temp/data000.npz', train=train, train_labels=train_labels)

        e2 = cv2.getTickCount()
        # calculate streaming duration
        time0 = (e2 - e1) / cv2.getTickFrequency()
        print 'Streaming duration:', time0

        print(train.shape)
        print(train_labels.shape)
        print 'Total frame:', total_frame
        print 'Saved frame:', saved_frame
        print 'Dropped frame', total_frame - saved_frame


    def close():
        # close connection
        self.conn.send("stop")
        conn.close()
        server_socket.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


ctd = CollectTrainingData()
ctd.connect()
ctd.start()
