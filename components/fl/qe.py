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

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.ports import FL as SERVER_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
##Adafruit_BBIO:
from Adafruit_I2C import Adafruit_I2C

#AtTiny  I2Cconnection
ATCON = Adafruit_I2C(0x04,2)

"""
###########################################################################
#                           Simulator setup                               #
###########################################################################

ATCON.setup_behavior('print')
"""

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
    arg["connection"].send_to_clients([int(ATCON.readU16(0))])


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["qe"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send medium integer unsigned (number of ticks)
SERVER.set_sending_datagram(['MEDIUM_INT_UNSIGNED'])

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
SERVER.listen_to_clients(request_cb, ARGUMENTS)
