import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
import gpioPinSettings


class Sensor(object):
    def init(self):
        print "Distance Measurement In Progress"

        GPIO.setup(FRONT_TRIGGER,GPIO.OUT)
        GPIO.setup(RIGHT_TRIGGER,GPIO.OUT)
        GPIO.setup(BACK_TRIGGER,GPIO.OUT)
        GPIO.setup(LEFT_TRIGGER,GPIO.OUT)
        GPIO.setup(ECHO_PIN,GPIO.IN)

        GPIO.output(FRONT_TRIGGER, False)
        GPIO.output(RIGHT_TRIGGER, False)
        GPIO.output(BACK_TRIGGER, False)
        GPIO.output(LEFT_TRIGGER, False)
        print "Waiting For Sensor To Settle"
        time.sleep(2)

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

        distance1 = measure(FRONT_TRIGGER,ECHO_PIN)
        time.sleep(0.05)
        distance2 = measure(RIGHT_TRIGGER,ECHO_PIN)
        time.sleep(0.05)
        distance3 = measure(BACK_TRIGGER,ECHO_PIN)
        time.sleep(0.05)
        distance4 = measure(LEFT_TRIGGER,ECHO_PIN)
        time.sleep(0.05)
        return distance1 +','+ distance2 +','+ distance3 +','+ distance4

    def exit(self):
        GPIO.setup(ECHO_PIN,GPIO.IN)

        GPIO.cleanup()
        
var = Sensor()
print var.distance()
