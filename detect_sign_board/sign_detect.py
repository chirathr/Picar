import cv2
import numpy as np

import time

kernel = np.ones((2, 2), np.uint8)

filters = [
    [np.array([0, 100, 100]), np.array([10, 255, 255])],        # Red stop sign
    [np.array([160, 100, 100]), np.array([180, 255, 255])],     # Red stop sign
]

font = cv2.FONT_HERSHEY_COMPLEX


def get_contours(hsv_sample, hsv_image):
    """
    return filtered contours from the two images
    :param hsv_sample:
    :param hsv_image:
    :return:
    """
    # filter out red from the two samples
    sample_in_range = cv2.inRange(hsv_sample, filters[0][0], filters[0][1])
    image_in_range = cv2.inRange(hsv_image, filters[1][0], filters[1][1])

    image_in_range = cv2.erode(image_in_range, kernel, iterations=1)
    image_in_range = cv2.dilate(image_in_range, kernel, iterations=2)

    img, sample_contours, hierarchy = cv2.findContours(sample_in_range, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img, image_contours, hierarchy = cv2.findContours(image_in_range, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return [sample_contours, image_contours]


def recognize(sample, image):                                      # recognize(sample, image)
    """
    recognize(sample, image)
    :param sample: Sample image
    :param image: The frame
    :return:
    """

    sign = None

    hsv_sample = cv2.cvtColor(sample, cv2.COLOR_BGR2HSV)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    sample_contours, image_contours = get_contours(hsv_sample, hsv_image)

    if len(image_contours) > 0:
        r = 0.0
        m = min(len(sample_contours), len(image_contours))
        for i in range(m):
            if i < len(sample_contours) and i < len(image_contours):
                r += cv2.matchShapes(sample_contours[i], image_contours[i], 1, 0.0)
        r = r / m
        print r
        if r < 0.05:
            cv2.drawContours(image, image_contours, -1, (0, 255, 0), 3)
            cv2.putText(image, 'Stop sign', (0, 130), font, 1, (0, 255, 0), 2)
            sign = "stop"
    cv2.imshow('frame', image)

    return sign


# # test to check for stop sign
# t0 = time.time()
#
# sample = cv2.imread('../images/stopPrototype.png')
# image = cv2.imread('../tutorial/road-stop.jpg')
#
# print recognize(sample, image)
# t1 = time.time()
# print("Execution time: " + str(t1 - t0))
#
# cv2.waitKey(0)
# cv2.destroyAllWindows()

