import numpy as np
import cv2
import glob
import sys


if len(sys.argv) != 2:
    print ("Error! usage: %s data0xx" % __file__)
    sys.exit()

e1 = cv2.getTickCount()

image_files = glob.glob('./image_data/' + sys.argv[1] + '/*.jpg')

image_data = np.zeros((1, 38400), dtype=np.float32)

for image_file in image_files:
    image = cv2.imread(image_file, 0)

    # get the lower half of the image
    roi = image[120:240, :]

    # convert img to a 1D array
    temp_array = roi.reshape(1, 38400).astype(np.float32)

    # stack image into rows
    image_data = np.vstack((image_data, temp_array))

image_data = image_data[1:-1]

print (image_data.shape)

print ('saving file as img-%s.npz' % sys.argv[1])

np.savez('./image_data/img-' + sys.argv[1] + '.npz', image_data=image_data)

e2 = cv2.getTickCount()

# calculate streaming duration
time0 = (e2 - e1) / cv2.getTickFrequency()
print ('time:', time0/60, ' mins')
