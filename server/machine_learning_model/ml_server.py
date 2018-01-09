import numpy
import cv2
import socket
import sys
from multiprocessing import Process


class SelfDrivingModel(Process):

    mlp_xml_path = 'mlp_xml/mlp.xml'

    def __init__(self, host='localhost', motor_port=8000, video_port=8001):
        super(SelfDrivingModel, self).__init__()

        # create two sockets
        self.video_address = (host, video_port)
        self.video_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.motor_address = (host, motor_port)
        self.motor_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.send_inst = True

        self.motor_connection = None
        self.video_connection = None

        self.model = None

    def connect(self):
        # create a server for the motor stream
        self.motor_server_socket.bind(self.motor_address)
        self.motor_server_socket.listen(5)
        self.motor_connection = self.motor_server_socket.accept()[0]
        print ("Connected to motor client")

        # server to get video stream from the car
        self.video_server_socket.bind(self.video_address)
        self.video_server_socket.listen(5)
        self.video_connection = self.video_server_socket.accept()[0].makefile('rb')
        print ("Connected to video client")

    def load_ann_mlp_model(self):
        # load ANN(Artificial Neural Networks) MLP (multi-layer perceptions)
        try:
            self.model = cv2.ml.ANN_MLP_load(self.mlp_xml_path)
            print ('Loading %s ' % self.mlp_xml_path)
        except RuntimeError:
            print ('Error loading file, check if file is found at %s' % self.mlp_xml_path)

    @staticmethod
    def direction_normalise(prediction):

        # [front, right, reverse, left]
        direction = numpy.zeros((1, 4), dtype=numpy.float32)

        # forward-left
        if prediction == 0:
            direction[0][0] = 1
            direction[0][3] = 1

        # forward
        if prediction == 1:
            direction[0][0] = 1

        # forward-right
        if prediction == 2:
            direction[0][1] = 1
            direction[0][3] = 1

        return direction

    def run(self):
        self.connect()
        print(self.motor_connection)

        # load the ann_mlp from file
        self.load_ann_mlp_model()

        # collect images for training
        print ('Start collecting images...')

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
                    roi = image[120:240, :]

                    # convert the lower half of image to 1D array
                    image_array = roi.reshape(1, 38400).astype(numpy.float32)

                    # Let the neural network make the prediction
                    prediction = self.model.predict(image_array)

                    # normalise direction to prevent errors
                    direction = self.direction_normalise(prediction[0])

                    data = str(int(direction[0][0])) + ',' + str(int(direction[0][1])) + ',' + \
                        str(int(direction[0][2])) + ',' + str(int(direction[0][3]))

                    # sent keyboard input to the motor controller
                    print (prediction, data)

                    self.motor_connection.send(data)

                    # display the image on screen
                    cv2.imshow('image', image)

        finally:
            self.close()

    def close(self):
        # close connection
        self.motor_connection.send("stop")
        self.motor_connection.close()

        # wait for a key and exit
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print ("Error! usage: %s host-ip motor-port" % __file__)
        sys.exit()
    ctd = SelfDrivingModel(sys.argv[1], int(sys.argv[2]), int(sys.argv[2]) + 1)
    ctd.start()
    ctd.join()
