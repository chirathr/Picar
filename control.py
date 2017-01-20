import RPi.GPIO as GPIO
import time


def setUp:
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

pwm.start(7)  #center
time.sleep(2)
pwm.ChangeDutyCycle(5) #right
time.sleep(2)
pwm.ChangeDutyCycle(9) #left
time.sleep(2)
pwm.ChangeDutyCycle(7) #center
time.sleep(2)
GPIO.cleanup()
