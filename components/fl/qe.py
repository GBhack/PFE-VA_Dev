"""
    qe.py
    Functional Level module : Quadratic Encoder manager
    Waits for a TCP request on its own port
    When gets a request, asks for an update from the Attiny
    through I2C and responds with the updated "ticks" count

"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import QE as QE_CS
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger

###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'

    from Adafruit_I2C import Adafruit_I2C

    #AtTiny  I2Cconnection
    ATCON = Adafruit_I2C(0x04, 2)
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    ROBOT_ROOT = open(path.expanduser('~/.robotConf'), 'r').read().strip().close()

    from Adafruit_I2C_SIM import Adafruit_I2C

    #AtTiny  I2Cconnection
    ATCON = Adafruit_I2C(0x04, 2)

    #Simulator setup
    ATCON.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > qe", ROBOT_ROOT+'logs/fl/')

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def request_cb(data, arg):
    """
        Callback function for quadratic encoder :
        Triggered when a request is received.
        Reads the quadratic encoder counter through
        I2C and responds to the request with the result.
    """
    #Responding the request with the obstacle presence status
    arg["connection"].send([int(ATCON.readU16(0))])


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(QE_CS, LOGGER)
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
SERVER.listen_to_clients(request_cb, ARGUMENTS)
SERVER.join_clients()
