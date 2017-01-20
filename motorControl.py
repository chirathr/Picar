import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
# select the pins
servoPin = 3
sp = 11
in1 = 5
in2 = 7
# set pins as outpu
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(sp, GPIO.OUT)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50)
speed = GPIO.PWM(sp, 50)
speed.start(30)
pwm.start(0)


def setUp():
    GPIO.setmode(GPIO.BOARD)
    # select the pins
    servoPin = 3
    sp = 11
    in1 = 5
    in2 = 7
    # set pins as output
    GPIO.setup(servoPin, GPIO.OUT)
    GPIO.setup(sp, GPIO.OUT)
    GPIO.setup(in1, GPIO.OUT)
    GPIO.setup(in2, GPIO.OUT)
    pwm = GPIO.PWM(servoPin, 50)
    speed = GPIO.PWM(sp, 50)
    speed.start(30)
    pwm.start(0)
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)

def forward():
    GPIO.output(in1, 1)
    GPIO.output(in2, 0)

def backward():
    GPIO.output(in1, 0)
    GPIO.output(in2, 1)

def stop():
    GPIO.output(in1, 0)
    GPIO.output(in2, 0)

def left():
    pwm.ChangeDutyCycle(9) #left
    print("left")

def right():
    pwm.ChangeDutyCycle(4.5)
    print("center")

def straight():
    pwm.ChangeDutyCycle(7) #center
    print("right")
