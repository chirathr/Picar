import cv2
import numpy
import sys


def check(prediction, label_truth):

    print (prediction, label_truth)

    if 3 > prediction >= 0:
        if label_truth[prediction] == 1:
            return 1
    else:
        print ('Error prediction should be between 0 and 2')
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
        output = model.predict(image_data[i:i+1])[0]
        correct += check(output, label_data[i].tolist())

    print ('Accuracy : %s' % str((correct * 100)/len(image_data)))
