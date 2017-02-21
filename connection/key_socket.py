#!/usr/bin/python                               # This is server.py file
import tty
import sys
import termios
import socket                                   # Import socket module

class Control(object):
    x = None
    steering = None
    running = None


    def __init__(self):
        self.x = 0
        self.steering = 1
        self.running = 1
        self.orig_settings = termios.tcgetattr(sys.stdin)
        tty.setraw(sys.stdin)

    def send_key(self, c):
        x = self.x
        steering = self.steering
        running = self.running
        while x != chr(27):                     # till ESC is pressed
            x = sys.stdin.read(1)[0]
            if x == 'a':
                if steering == 2:
                    c.send('straight');
                    steering = 1
                else:
                    c.send('A')
                    steering = 0
            if x == 'd':
                if(steering == 0):
                    c.send('straight')
                    steering = 1
                else:
                    c.send('D')
                    steering = 2

            if x == 'w':
            	if running == 2:
            	    c.send("stop")
            	    running = 1
            	else:
            	    c.send("W")
            	    running = 0
            if x == 's':
            	if running == 0:
            	    c.send("stop")
            	    running = 1
            	else:
                    c.send('S')
            	    running = 2

        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, orig_settings)


class SocketServer(object):
    s = None
    c = None

    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        host = socket.gethostname()      # Get local machine name
        port = 12347                     # Reserve a port for your service.
        self.s.bind((host, port))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection

    def close(self):
        c.close()

    def connect(self):
        self.c, addr = self.s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        self.c.send('connection sucessfull')

    def start_sending(self):
        control = Control()
        control.send_key(self.c);
