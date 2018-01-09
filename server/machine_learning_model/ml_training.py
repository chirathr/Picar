import numpy as np
import cv2
import sys
import glob
import os


class MLModel(object):
    def __init__(self):
        self.image_array = np.zeros((1, 38400), dtype=np.float32)
        self.label_array = np.zeros((1, 3), dtype=np.float32)

        self.training_data_base_url = '../training_data/'

    def load_all_training_data(self):
        # start timer
        t0 = cv2.getTickCount()

        # load all the label data

        label_files = glob.glob(self.training_data_base_url + 'label_data/*.npz')

        for label_file in label_files:
            self.label_array = np.vstack((self.label_array, np.load(label_file)['label_data']))

            self.image_array = np.vstack((self.image_array, np.load(
                self.training_data_base_url + 'image_data/img-' + label_file[-11:])['image_data']))
            print (label_file)
            print self.image_array.shape
            print self.label_array.shape

        print ('All labels loaded successfully')
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
        model.setLayerSizes(np.int32([38400, 32, 3]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001))

        self.load_all_training_data()

        mlp_file = glob.glob('./mlp_xml/*.xml')

        if len(mlp_file) > 0:
            print ('MLP data already found: ' + mlp_file[0])
            model = cv2.ml.ANN_MLP_load(mlp_file[0])
            print ('IsTrained : ' + str(model.isTrained()))
        else:
            if not os.path.exists('./mlp_xml/'):
                os.makedirs('./mlp_xml/')

        print 'Training MLP ...'
        print (self.image_array.shape, self.label_array.shape)
        num_iter = model.train(self.image_array, cv2.ml.ROW_SAMPLE, self.label_array)

        t1 = cv2.getTickCount()

        time = (t1 - t0) / cv2.getTickFrequency()
        print 'Training complete in :', time

        # save param
        model.save('./mlp_xml/mlp.xml')

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
