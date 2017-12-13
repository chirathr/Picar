import numpy as np
import cv2
import glob


class MLModel(object):
    def __inti__(self):
        self.image_array = np.zeros((1, 38400))
        self.label_array = np.zeros((1, 4), dtype = np.float32)


    def load_training_data(self, image_path, label_path):
        t0 = cv2.getTickCount()
        images = glob.glob(image_path)
        label_data = np.load(label_path)['train_labels']
        image_data = np.zeros((1, 38400), dtype = np.float32)

        for image in images:
            img = cv2.imread(image, 0)
            roi = img[120:240, :]
            temp_array = roi.reshape(1, 38400).astype(np.float32)
            image_data = np.vstack((image_data, temp_array))

        self.image_array = image_data[1:30]
        self.label_array = label_data[1:30]

        print self.image_array.shape
        print self.label_array.shape

        t1 = cv2.getTickCount()

        time = (t1 - t0)/ cv2.getTickFrequency()
        print 'Image loaded in :', time

    def start(self):
        t0 = cv2.getTickCount()

        # create MLP
        model = cv2.ml.ANN_MLP_create()
        model.setTrainMethod(cv2.ml.ANN_MLP_RPROP | cv2.ml.ANN_MLP_UPDATE_WEIGHTS)
        model.setLayerSizes(np.int32([38400, 32, 4]))
        model.setActivationFunction(cv2.ml.ANN_MLP_SIGMOID_SYM)
        model.setTermCriteria((cv2.TERM_CRITERIA_COUNT | cv2.TERM_CRITERIA_EPS, 500, 0.0001))

        self.load_training_data('../training_images/*.jpg', '../training_data/data000.npz')

        print 'Training MLP ...'
        print (self.image_array.shape, self.label_array.shape)
        num_iter = model.train(self.image_array, cv2.ml.ROW_SAMPLE, self.label_array)

        t1 = cv2.getTickCount()

        time = (t1 - t0)/ cv2.getTickFrequency()
        print 'Training complete in :', time

        # save param
        model.save('mlp_xml/mlp.xml')

        print 'Ran for %d iterations' % num_iter

        ret, resp = model.predict(self.image_array)
        prediction = resp.argmax(-1)
        print 'Prediction:', prediction
        true_labels = self.label_array.argmax(-1)
        print 'True labels:', true_labels

        print 'Testing...'
        train_rate = np.mean(prediction == true_labels)
        print 'Train rate: %f:' % (train_rate*100)


mlmodel = MLModel()
mlmodel.start()
