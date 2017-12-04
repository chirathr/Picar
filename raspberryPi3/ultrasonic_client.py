import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)

TRIG1 = 31
TRIG2 = 33
TRIG3 = 35
TRIG4 = 37
ECHO = 29
def initial():
	print "Distance Measurement In Progress"

	GPIO.setup(TRIG1,GPIO.OUT)
	GPIO.setup(TRIG2,GPIO.OUT)
	GPIO.setup(TRIG3,GPIO.OUT)
	GPIO.setup(TRIG4,GPIO.OUT)
	GPIO.setup(ECHO,GPIO.IN)

	GPIO.output(TRIG1, False)
	GPIO.output(TRIG2, False)
	GPIO.output(TRIG3, False)
	GPIO.output(TRIG4, False)
	print "Waiting For Sensor To Settle"
	time.sleep(2)
	
	
def measure(TRIG,ECHO):
	

	GPIO.output(TRIG, True)
	time.sleep(0.00001)
	GPIO.output(TRIG, False)

	while GPIO.input(ECHO)==0:
		pulse_start = time.time()

	while GPIO.input(ECHO)==1:
		pulse_end = time.time()

	pulse_duration = pulse_end - pulse_start

	distance = pulse_duration * 17150

	distance = round(distance, 2)
	return distance
initial()
while True:
	distance1 = measure(TRIG1,ECHO)
	time.sleep(0.05)	
	distance2 = measure(TRIG2,ECHO)
	time.sleep(0.05)
	distance3 = measure(TRIG3,ECHO)
	time.sleep(0.05)
	distance4 = measure(TRIG4,ECHO)
	time.sleep(0.05)
	print distance1 ,',', distance2 ,',', distance3 ,',', distance4

GPIO.setup(ECHO,GPIO.IN)

GPIO.cleanup()
