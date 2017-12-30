import numpy as np
import cv2 as cv
import glob
import sys


if len(sys.argv) != 4:
    print("Usage: %s path_to_images/ height width")
    sys.exit(0)
else:
    frame = 1
    images = glob.glob(sys.argv[1] + '*.jpg')
    for image in images:
        img = cv.imread(image, 0)
        resized_img = cv.resize(img, (int(sys.argv[2]), int(sys.argv[3])))
        print(image)
        cv.imwrite(sys.argv[1] + 'frame{:>05}.jpg'.format(frame), resized_img)
        frame += 1
    print("resize completed")
