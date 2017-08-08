import cv2
import numpy as np

frame = cv2.imread('../images/roas-Stop-Sign.jpg')


lower_red = np.array([160, 100, 100])
upper_red = np.array([180, 255, 255])

font = cv2.FONT_HERSHEY_COMPLEX


img = cv2.imread('../images/stopPrototype.png')
hsv_stop = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
stop = cv2.inRange(hsv_stop, np.array([0, 100, 100]), np.array([10, 255, 255]))

im1, stop_shape, hierarchy = cv2.findContours(stop, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


# Convert BGR to HSV
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

# define range of blue color in HSV

mask = cv2.inRange(hsv, lower_red, upper_red)

# noise reduction

kernel = np.ones((2, 2), np.uint8)
erosion = cv2.erode(mask, kernel, iterations=1)
kernel = np.ones((2, 2), np.uint8)
dilation = cv2.dilate(erosion, kernel, iterations=1)

im2, contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# cv2.imshow('frame', frame)
# cv2.imshow('mask', mask)
# cv2.imshow('erode', dilation)

if len(contours) > 0:
    r = 0.0
    m = min(len(contours), len(stop_shape))
    for i in range(m):
        if i < len(contours) and i < len(stop_shape[i]):
            r += cv2.matchShapes(contours[i], stop_shape[i], 1, 0.0)
    r = r / len(contours)
    if r < 0.3:
        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
        cv2.putText(frame, 'Stop sign', (0, 130), font, 1, (0, 255, 0), 2)

cv2.imshow('frame', frame)

cv2.waitKey(0)
cv2.destroyAllWindows()
