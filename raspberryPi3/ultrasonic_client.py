from socket import *
import time
import RPi.GPIO as GPIO


GPIO.setwarnings(False)

# create a socket and bind socket to the host
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(('192.168.1.100', 8002))

def measure(GPIO_TRIGGER):
    """
    measure distance
    """
    GPIO.output(GPIO_TRIGGER, True)
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
    start = time.time()

    while GPIO.input(GPIO_ECHO)==0:
        start = time.time()

    while GPIO.input(GPIO_ECHO)==1:
        stop = time.time()

    elapsed = stop-start
    distance = (elapsed * 34300)/2

    return distance

# referring to the pins by GPIO numbers
GPIO.setmode(GPIO.BCM)

# define pi GPIO
GPIO_TRIGGER1 = 31          #Front
GPIO_TRIGGER2 = 33          #Right
GPIO_TRIGGER3 = 35          #Back
GPIO_TRIGGER4 = 37          #Left
GPIO_ECHO     = 29

# output pin: Trigger
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)
# input pin: Echo
GPIO.setup(GPIO_ECHO,GPIO.IN)
# initialize trigger pin to low
GPIO.output(GPIO_TRIGGER, False)

try:
    while True:
        distance1 = measure(GPIO_TRIGGER1)
        time.sleep(0.1)
        print "Distance : %.1f cm" % distance
        distance2 = measure(GPIO_TRIGGER2)
        time.sleep(0.1)
        print "Distance : %.1f cm" % distance
        distance3 = measure(GPIO_TRIGGER3)
        time.sleep(0.1)
        print "Distance : %.1f cm" % distance
        distance4 = measure(GPIO_TRIGGER4)
        time.sleep(0.1)
        print "Distance : %.1f cm" % distance
        # send data to the host every 0.5 sec
        client_socket.send(str(distance1+","+distance2+","+distance3+","+distance4))
        time.sleep(0.5)
finally:
    client_socket.close()
    GPIO.cleanup()
