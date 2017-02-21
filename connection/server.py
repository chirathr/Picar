#!/usr/bin/python                               # This is server.py file
import tty
import sys
import socket         # Import socket module
import sys
import os
from Tkinter import *
os.system('xset r off')



class Control(object):
    x = None
    steering = None
    running = None

    def __init__(self):
        self.x = 0
        self.steering = 1
        self.running = 1


    def send_key(self, c):
        x = self.x
        steering = self.steering
        running = self.running
        print "done"

        def keyup(e):
    	    c.send(e.char + '.' + 'key-up')
        def keydown(e):
     	    c.send(e.char + '.' + 'key-down')

        root = Tk()

        frame = Frame(root, width=100, height=100)
        frame.bind("<KeyPress>", keydown)
        frame.bind("<KeyRelease>", keyup)
        frame.pack()
        frame.focus_set()
        root.mainloop()
        c.close()




class SocketServer(object):
    s = None
    c = None
    host = None
    port = 0

    def __init__(self):
        self.s = socket.socket()         # Create a socket object
        self.host = socket.gethostname()      # Get local machine name

    def close(self):
        c.close()

    def connect(self, port):
        self.port = port                    # Reserve a port for your service.
        self.s.bind(('', self.port))        # Bind to the port
        self.s.listen(5)                 # Now wait for client connection
        self.c, addr = self.s.accept()     # Establish connection with client.
        print 'Got connection from', addr
        self.c.send('connection sucessfull')

    def start_sending(self):
        control = Control()
        control.send_key(self.c);
