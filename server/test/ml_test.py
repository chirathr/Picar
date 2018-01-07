import cv2
import numpy
import sys


def direction_normalise(prediction):
    # [front, right, reverse, left]
    direction = numpy.zeros((1, 4), dtype=numpy.float32)

    for i in range(4):
        if prediction[0][i] > 0:
            direction[0][i] = 1

    return direction


def check(label_predicted, label_truth):

    # print (label_predicted, label_truth)

    if label_predicted == label_truth:
        return 1
    return 0


if len(sys.argv) != 2:
    print ('Usage: %s data00x' % __file__)
    sys.exit(0)
else:
    model = cv2.ml.ANN_MLP_create()
    model = model.load('../machine_learning_model/mlp_xml/mlp.xml')

    image_data = numpy.load('../training_data/image_data/img-' + sys.argv[1] + '.npz')['image_data']
    label_data = numpy.load('../training_data/label_data/' + sys.argv[1] + '.npz')['train_labels'][:-1]

    correct = 0

    for i in range(len(image_data)):
        output = model.predict(image_data[i:i+1])[1]

        print (direction_normalise(output), label_data[i])

        correct += check(direction_normalise(output)[0].tolist(), label_data[i].tolist())

    print ('Accuracy : %s' % str((correct * 100)/len(image_data)))
