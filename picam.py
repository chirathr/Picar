import cv2
import numpy as np

from picamera.array import PiRGBArray
from picamera import PiCamera
import time

from detect_sign_board.sign_detect import *
from motor.motorControl import *

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
rawCapture = PiRGBArray(camera)

# allow the camera to warm up
time.sleep(0.1)

cam = cv2.VideoCapture(0)

sample = cv2.imread('../images/stopPrototype.png')

motor = Motor()

while True:
    # grab an image from the camera
    camera.capture(rawCapture, format="bgr")
    frame = rawCapture.array

    if recognize(sample, frame) == 'stop':
        motor.stop()
    else:
        motor.forward()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        motor.stop()
        break

cam.release()
cv2.destroyAllWindows()
