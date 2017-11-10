import RPi.GPIO as GPIO
import time
from gpioPinSettings import IN1, IN2, SPEED, SERVO


class Motor(object):
    """
    The class has methods to control Picar, The method input takes the parameters
    0 - stop
    1 - forward
    2 - backward
    3 - left
    4 - center
    5 - right
    """
    def __init__(self):
        # set the pin layout
        GPIO.setmode(GPIO.BOARD)

        # select the pins
        self.servoPin = SERVO
        self.sp = SPEED
        self.in1 = IN1
        self.in2 = IN2

        # set pins as output
        GPIO.setup(self.servoPin, GPIO.OUT)
        GPIO.setup(self.sp, GPIO.OUT)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

        # set servo and speed pin as PWM pins
        self.pwm = GPIO.PWM(self.servoPin, 50)
        self.speed = GPIO.PWM(self.sp, 50)
        self.speed.start(50)
        self.pwm.start(0)

        # stop and center the car initially
        self.stop()
        self.center()

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

    def input(self, inp):
        if inp == 0:
            self.stop()
        elif inp == 1:
            self.forward()
        elif inp == 2:
            self.backward()
        elif inp == 3:
            self.left()
        elif inp == 4:
            self.straight()
        elif inp == 5:
            self.right()
        else:
            print("Wrong input to motor controller, choices are (0-5)")
