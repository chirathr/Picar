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
        self.speed.start(60)
        self.pwm.start(0)

        # stop and center the car initially
        self.stop()
        self.straight()

        # direction variable
        self.direction = [0, 0, 0, 0]

    def speed(self, value):
        """
        Speed between 0 and 10
        """
        if value <= 10 or value >= 0:
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

    def left(self):
        self.pwm.ChangeDutyCycle(9)  # left
        print("left")

    def right(self):
        self.pwm.ChangeDutyCycle(4.5)  # right
        print("right")

    def straight(self):
        self.pwm.ChangeDutyCycle(7)  # straight
        print("straight")

    def drive(self, direction):
        """
        :param direction: [forward, right, backward, left]
        :return:
        """
        print(self.direction, direction, " ", self.direction != direction)

        if self.direction != direction:
            self.direction = direction[:]

            # center
            if direction[1] == 0 and direction[3] == 0:
                self.straight()

            # stop
            if direction[0] == 0 and direction[2] == 0:
                self.stop()

            # multiple commands
            if direction[0] == 1:
                self.forward()
                if direction[1] == 1:
                    self.right()
                if direction[3] == 1:
                    self.left()
            elif direction[2] == 1:
                self.backward()
                if direction[1] == 1:
                    self.right()
                if direction[3] == 1:
                    self.left()
            else:
                if direction[1] == 1:
                    self.right()
                if direction[3] == 1:
                    self.left()

    @staticmethod
    def close():
        GPIO.cleanup()
