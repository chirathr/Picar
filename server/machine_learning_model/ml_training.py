import numpy as np
import cv2
import glob


class MLModel(object):
    def __init__(self):
        self.image_array = np.zeros((1, 38400), dtype=np.float32)
        self.label_array = np.zeros((1, 4), dtype=np.float32)
        self.image_data = np.zeros((1, 38400), dtype=np.float32)

    def load_training_data(self, image_path, label_path):
        """
            This function takes all the images from the image path and converts
            to an numpy float32 array. It also loads the saved label data.
        """
        # start timer
        t0 = cv2.getTickCount()

        # get all the jpeg images in the path
        images = glob.glob(image_path)

        # load all the label data
        self.label_array = np.load(label_path)['train_labels']

        # convert all images to numpy float32 array and stack them
        for image in images:
            # read an image
            img = cv2.imread(image, 0)

            # get the lower half of the image
            roi = img[120:240, :]

            # convert img to a 1D array
            temp_array = roi.reshape(1, 38400).astype(np.float32)

            # stack image into rows
            self.image_data = np.vstack((self.image_data, temp_array))

        self.image_array = self.image_data[1:-1]
        self.label_array = self.label_array[1:]

        print self.image_array.shape
        print self.label_array.shape

        # end timer
        t1 = cv2.getTickCount()

        # print the time to load the image
        time = (t1 - t0) / cv2.getTickFrequency()
        print 'Image loaded in :', time

    def start(self):
        """
            Takes the label_array and image_array trains the ANN_MLP network.
        """
        t0 = cv2.getTickCount()

        # create ANN(Artificial Neural Networks) MLP (multi-layer perceptrons)
        model = cv2.ml.ANN_MLP_create()

        # Train method as
        model.setTrainMethod(cv2.ml.ANN_MLP_RPROP | cv2.ml.ANN_MLP_UPDATE_WEIGHTS)
        model.setLayerSizes(np.int32([38400, 32, 4]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001))

        self.load_training_data('../training_images/*.jpg', '../training_data/data000.npz')

        print 'Training MLP ...'
        print (self.image_array.shape, self.label_array.shape)
        num_iter = model.train(self.image_array, cv2.ml.ROW_SAMPLE, self.label_array)

        t1 = cv2.getTickCount()

        time = (t1 - t0) / cv2.getTickFrequency()
        print 'Training complete in :', time

        # save param
        model.save('../mlp_xml/mlp.xml')

        print 'Ran for %d iterations' % num_iter

        ret, resp = model.predict(self.image_array)
        prediction = resp.argmax(-1)
        print 'Prediction:', prediction
        true_labels = self.label_array.argmax(-1)
        print 'True labels:', true_labels

        print 'Testing...'
        train_rate = np.mean(prediction == true_labels)
        print 'Train rate: %f:' % (train_rate * 100)


ml_model = MLModel()
ml_model.start()
