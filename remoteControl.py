import tty
import sys
import termios

orig_settings = termios.tcgetattr(sys.stdin)

tty.setraw(sys.stdin)
x = 0
while x != chr(27): # till ESC is pressed
    x=sys.stdin.read(1)[0]
    print("You pressed", x)
    

termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)
