import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

# select the pins
servoPin = 11

GPIO.setup(servoPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50)

pwm.start(7)  #center
time.sleep(2)
pwm.ChangeDutyCycle(5) #right 
time.sleep(2)
pwm.ChangeDutyCycle(9) #left
time.sleep(2)
pwm.ChangeDutyCycle(7) #center
time.sleep(2)
GPIO.cleanup()
