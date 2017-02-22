import RPi.GPIO as GPIO
import time


class Motor(object):

    # select the pins
    servoPin = 0
    sp = 0
    in1 = 0
    in2 = 0

    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        # select the pins
        self.servoPin = 3
        self.sp = 11
        self.in1 = 5
        self.in2 = 7
        # set pins as output
        GPIO.setup(self.servoPin, GPIO.OUT)
        GPIO.setup(self.sp, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        pwm = GPIO.PWM(self.servoPin, 50)
        speed = GPIO.PWM(self.sp, 50)
        speed.start(50)
        pwm.start(0)
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 0)

    def forward(self):
        GPIO.output(self.in1, 1)
        GPIO.output(self.in2, 0)

    def backward(self):
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 1)

    def stop(self):
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 0)

    def left(self):
        pwm.ChangeDutyCycle(9) #left
        print("left")

    def right(self):
        pwm.ChangeDutyCycle(4) # right
        print("center")

    def straight(self):
        pwm.ChangeDutyCycle(7.5) #center
        print("right")

    def input(self, x):
        if x == 'a.key-down':
            left()
        if x == 'a.key-up':
            straight()
        if x == 'w.key-down':
            forward()
        if x == 'w.key-up':
            stop()
        if x == 'd.key-down':
            right()
        if x == 'd.key-up':
            straight()
        if x == 's.key-down':
            backward()
        if x == 's.key-up':
            stop()
