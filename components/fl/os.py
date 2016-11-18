"""
    os.py
    Functional Level module : Optical Sensors manager
    Waits for a TCP request on its own port
    When gets a request, responds with a binary state
    of the seven reflective sensors (1 for white line, or 0)
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import atexit
import time


#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
from robotBasics.constants import ports as PORTS
from robotBasics.constants.misc import OS as MISC
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
import Adafruit_BBIO.ADC as ADC

###########################################################################
#                           Simulator setup                               #
###########################################################################

ADC.setup_behavior('print')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
ADC.setup()

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def readSingleSensor(sensor):
    return ADC.read(sensor) > MISC["threshold"]

def read_array_cb(data, arg):
    """
        Callback function for reflective sensor array reading :
        Triggered when a request is received.
        Responds with a 7 bit array describing the array of
        sensor's state (1 for a line detected, or 0)
    """
    array = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        array[i]=int(readSingleSensor(GPIODEF.OS[i]))
    #Responding the request with the button pushing status
    arg["connection"].send_to_clients([array])


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(PORTS.FL["os"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send bool
SERVER.set_sending_datagram([['BITS', [1,1,1,1,1,1,1]]])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : SERVER
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(read_array_cb, ARGUMENTS)
