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
        self.pwm = GPIO.PWM(self.servoPin, 50)
        self.speed = GPIO.PWM(self.sp, 50)
        self.speed.start(50)
        self.pwm.start(0)
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
        self.pwm.ChangeDutyCycle(9) #left
        print("left")

    def right(self):
        self.pwm.ChangeDutyCycle(4) # right
        print("center")

    def straight(self):
        self.pwm.ChangeDutyCycle(7.5) #center
        print("right")

    def input(self, x):
        if x == 'a.key-down':
            self.left()
        if x == 'a.key-up':
            self.straight()
        if x == 'w.key-down':
            self.forward()
        if x == 'w.key-up':
            self.stop()
        if x == 'd.key-down':
            self.right()
        if x == 'd.key-up':
            self.straight()
        if x == 's.key-down':
            self.backward()
        if x == 's.key-up':
            self.stop()
