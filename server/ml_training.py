import numpy as np
import cv2
import glob


class MLModel(object):
    def __inti__(self):
        self.image_array = np.zeros((1, 38400))
        self.label_array = np.zeros((1, 4), 'int')


    def load_training_data(self, image_path, label_path):
        images = glob.glob(image_path)
        label_data = np.load(label_path)['train_labels']
        image_data = np.zeros((1, 38400))

        for image in images:
            img = cv2.imread(image, 0)
            roi = img[120:240, :]
            temp_array = roi.reshape(1, 38400).astype(np.float32)
            image_data = np.vstack((image_data, temp_array))

        print image_data.shape
        print label_data.shape
        return [image_data, label_data]



mlmodel = MLModel()

data = mlmodel.load_training_data('../training_images/*.jpg', '../training_data/data000.npz')
print data
