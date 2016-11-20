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

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import OS as OS_GPIO
from robotBasics.constants.ports import FL as SERVER_PORTS
from robotBasics.constants.misc import OS as MISC
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
##Adafruit_BBIO:
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
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["os"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send bool
SERVER.set_sending_datagram([['BITS', [1, 1, 1, 1, 1, 1, 1]]])

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
