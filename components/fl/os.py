"""
    os.py
    Functional Level module : Optical Sensors manager
    Waits for a TCP request on its own port
    When gets a request, responds with a binary state
    of the seven reflective sensors (1 for white line, or 0)
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import OS as OS_GPIO
from robotBasics.constants.connectionSettings import OS as OS_CS
from robotBasics.constants.misc import OS as MISC
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger
##Adafruit_BBIO:
import Adafruit_BBIO.ADC as ADC

###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot'
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    ROBOT_ROOT = open(path.expanduser('~/.robotConf'), 'r').read().strip().close()

    #Simulator setup
    ADC.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > os", ROBOT_ROOT+'logs/fl/')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
ADC.setup()

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def read_single_sensor(sensor):
    """
        Reads the analog value from a specific reflective sensor
        and returns "True" if this value is higher than the threshold
        (possible white line) and False in the other case (no white line)
    
    Arguments:
        sensor {string} -- GPIO pin name
    
    Returns:
        Boolean -- line detection status
    """
    return ADC.read(sensor) > MISC["threshold"]

def read_array_cb(data, arg):
    """
        Callback function for reflective sensor array reading :
        Triggered when a request is received.
        Responds with a 7 bit array describing the array of
        sensor's state (1 for a line detected, or 0)
    
    Arguments:
        data {array} -- Decoded data directly from the received request
        arg  -- Reference to a list of predifined arguments (to synchronize with the main thread)
    """
    array = []   #Initialization

    for i in range(7):
        array.append(int(read_single_sensor(OS_GPIO[i])))

    #Responding the request with the button pushing status
    arg["connection"].send_to_clients([array])


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                       #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(OS_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "connection" : SERVER
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(read_array_cb, ARGUMENTS)
