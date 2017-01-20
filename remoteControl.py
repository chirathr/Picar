import tty
import sys
import termios
from motorControl import *

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)

setUp()

x = 0
steering = 1
running = 1

while x != chr(27): # till ESC is pressed
    x=sys.stdin.read(1)[0]
    print("You pressed", x)
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

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
GPIO.cleanup()
