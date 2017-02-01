"""
    pb.py
    Functional Level module : PushButton manager
    Keeps track of the pushbutton's history
    Waits for a TCP request on its own port
    When gets a request, responds with True if
    the button has been pushed since last request
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
import time
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import RESET as RESET_GPIO
from robotBasics.constants.connectionSettings import PB as PB_CS
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger

###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'
    import Adafruit_BBIO.GPIO as GPIO
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()

    import Adafruit_BBIO_SIM.GPIO as GPIO

    #Simulator setup
    GPIO.pin_association(RESET_GPIO, 'pushbutton\'s state')
    GPIO.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > pb", ROBOT_ROOT+'logs/fl/')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
GPIO.setup(RESET_GPIO, GPIO.IN)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def pb_update_cb(data, arg):
    """
        Callback function for push button status reading :
        Triggered when a request is received.
        Responds True if the button has been pushed since last
        request and then reset the button's status
    """
    #Responding the request with the button pushing status
    arg["connection"].send([arg["state"]])
    #Reseting the button pushing status
    arg["state"] = False


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(PB_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "connection" : SERVER,
    "state" : False
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(pb_update_cb, ARGUMENTS)

LOOPING = True

while LOOPING:
    try:
        if not GPIO.input(RESET_GPIO):
            while not GPIO.input(RESET_GPIO):
                time.sleep(0.1)
            ARGUMENTS['state'] = True
        time.sleep(0.5)
    except:
        LOOPING = False