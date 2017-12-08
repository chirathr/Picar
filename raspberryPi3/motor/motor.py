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
        self.straight()

    def speed(self, value):
        """
        Speed between 0 and 10
        """
        if (value <= 10 or value >= 0):
            self.speed.start(value * 10)
        else:
            print("Speed should be between 0 and 10")

    def forward(self):
        GPIO.output(self.in1, 1)
        GPIO.output(self.in2, 0)

    def backward(self):
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 1)

    def stop(self):
        GPIO.output(self.in1, 0)
        GPIO.output(self.in2, 0)

    def manual_direction(self, value):
        """
        value in the range(0, 6)
        """
        value = 5 - value   # so that left = 0 and right = 5
        if (value > 5 or value < 0):
            print("Direction values should be between 0 and 5")
        else:
            self.pwm.ChangeDutyCycle(4 + value)

    def left(self):
        self.manual_direction(0) #left

    def right(self):
        self.manual_direction(5) # right

    def straight(self):
        self.manual_direction(3.5) # straight

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

    def drive(self, direction):
        if (direction[0] == 0 and direction[1] == 0):
            self.straight()
        if (direction[2] == 0 and direction[3] == 0):
            self.stop()

        if (direction[0] == 1):
            self.left()
        if (direction[1] == 1):
            self.right()
        if (direction[2] == 1):
            self.forward()
        if (direction[3] == 1):
            self.backward()

    def close(self):
        GPIO.cleanup()
