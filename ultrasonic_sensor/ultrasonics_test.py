import RPi.GPIO as GPIO                    #Import GPIO library
import time                                #Import time library
GPIO.setmode(GPIO.BOARD)                   #Set GPIO pin numbering


class Ultrasonic(object):
    ECHO = 23                                    #Associate pin 23 to ECHO
    F = 13                                       #Front trigger pin
    B = 19                                       #Back trigger pin
    L = 21                                       #Left trigger pin
    R = 15                                       #Right trigger pin

    def __init__():
        GPIO.setup(self.TRIG,GPIO.OUT)           #Set pin as GPIO out
        GPIO.setup(self.ECHO,GPIO.IN)            #Set pin as GPIO in
        GPIO.setup(self.TRIG2,GPIO.OUT)


    def dist(TRIG):
        GPIO.output(TRIG, False)                 #Set TRIG as LOW
        time.sleep(.00001)                       #Delay

        GPIO.output(TRIG, True)                  #Set TRIG as HIGH
        time.sleep(0.00001)                      #Delay of 0.00001 seconds
        GPIO.output(TRIG, False)                 #Set TRIG as LOW

        while GPIO.input(self.ECHO)==0:          #Check whether the ECHO is LOW
            pulse_start = time.time()            #Saves the last known time of LOW pulse

        while GPIO.input(self.ECHO)==1:          #Check whether the ECHO is HIGH
            pulse_end = time.time()              #Saves the last known time of HIGH pulse

        pulse_duration = pulse_end - pulse_start #Get pulse duration to a variable

        distance = pulse_duration * 17150        #Multiply pulse duration by 17150 to get distance
        distance = round(distance, 2)            #Round to two decimal points

        if distance > 2 and distance < 400:      #Check whether the distance is within range
            return distance - 0.5                #Print distance with 0.5 cm calibration
        else:
            return -1

    def dist_all(self):                              # return all sensor data
        return str(
        dist(self.F) + ',' +
        dist(self.B) + ',' +
        dist(self.L) + ',' +
        dist(self.R))

    def front(self):
        return dist(self.F)

    def back(self):
        return dist(self.B)

    def left(self):
        return dist(self.L)

    def right(self):
        return dist(self.R)
