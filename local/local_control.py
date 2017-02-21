import tty
import sys
import termios

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)

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
speed = GPIO.PWM(sp, 100)
speed.start(50)
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


x = 0
steering = 1
running = 1

while x != chr(27): # till ESC is pressed
    x=sys.stdin.read(1)[0]
    if x == 'a':
        if steering == 2:
            straight()
            steering = 1
        else:
            left()
            steering = 0
    if x == 'd':
        if(steering == 0):
            straight()
            steering = 10
        else:
            right()
            steering = 2

    if x == 'w':
	if running == 2:
	    stop()
	    running = 1
	else:
	    forward()
	    running = 0
    if x == 's':
	if running == 0:
	    stop()
	    running = 1
	else:
        backward()
	    running = 2

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
GPIO.cleanup()
