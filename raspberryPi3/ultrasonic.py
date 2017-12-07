import RPi.GPIO as GPIO
import time
from gpioPinSettings import *


class Ultrasonic(object):
    def __init__(self):
        print("setting up pins")
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(FRONT_TRIGGER, GPIO.OUT)
        GPIO.setup(RIGHT_TRIGGER, GPIO.OUT)
        GPIO.setup(BACK_TRIGGER, GPIO.OUT)
        GPIO.setup(LEFT_TRIGGER, GPIO.OUT)
        GPIO.setup(ECHO_PIN, GPIO.IN)

        GPIO.output(FRONT_TRIGGER, False)
        GPIO.output(RIGHT_TRIGGER, False)
        GPIO.output(BACK_TRIGGER, False)
        GPIO.output(LEFT_TRIGGER, False)

        print("Waiting For Sensor To Settle")
        time.sleep(1)

    def measure(self,TRIG,ECHO_PIN):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO_PIN)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO_PIN)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance = pulse_duration * 17150

        distance = round(distance, 2)
        return distance

    def distance(self):
        front = self.measure(FRONT_TRIGGER, ECHO_PIN)
        time.sleep(0.025)
        right = self.measure(RIGHT_TRIGGER, ECHO_PIN)
        time.sleep(0.025)
        back = self.measure(BACK_TRIGGER, ECHO_PIN)
        time.sleep(0.025)
        left = self.measure(LEFT_TRIGGER, ECHO_PIN)
        time.sleep(0.025)
        print([front, right, back, left])
        return [front, right, back, left]

    def close(self):
        GPIO.setup(ECHO_PIN,GPIO.IN)
        GPIO.cleanup()

var = Ultrasonic()
print var.distance()
