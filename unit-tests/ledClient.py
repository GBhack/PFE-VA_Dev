"""
    ledc.py
    LEDs Controller
    Manage the LED's state
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-


###Standard imports :
import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import LED as LED_CS
from robotBasics.constants.connectionSettings import LEDC as LEDC_CS
from robotBasics.constants.gpiodef import LEDS_STATE as LEDS_STATE
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.logger import robotLogger


###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("ECL > ledc", ROBOT_ROOT+'logs/ecl/')

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def request_cb(data, args):
    """
        Callback function for ultrasonic sensor controler:
        Triggered when a request is received.
        Update the obstacle detection status and responds to
        the request with the updated status.
    """
    print('RANK : ')
    print(data[0][0])
    if args["LEDs_state"][data[0][0]] != bool(data[0][1]):
        args["LEDs_state"][data[0][0]] = bool(data[0][1])
        args["client"].send([args["LEDs_state"]])
        args["server"].send([args["client"].receive()[0]])
    else:
        args["server"].send([True])
    print(args["LEDs_state"])

###########################################################################
#                   CONNECTIONS SET UP AND SETTINGS :                     #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = Client(LED_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#Opening the connection
CLIENT.connect()

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(LEDC_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

#Argument to be passed to the steering callback method
ARGUMENTS = {
    "server": SERVER,
    "client": CLIENT,
    "LEDs_state": LEDS_STATE
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and redirecting them to the callback methods
SERVER.listen_to_clients(request_cb, ARGUMENTS)
SERVER.join_clients()
