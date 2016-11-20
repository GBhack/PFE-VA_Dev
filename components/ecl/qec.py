"""
    qec.py
    Execution Control Level module : Quadratic Encoder Controler
    Waits for a TCP request on its own port
    When gets a request, asks (if necessary) for an update from the
    Quadratic Encoder FL module and responds with the updated "ticks" count.

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
from time import time

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.ports import FL as CLIENTS_PORTS
from robotBasics.constants.ports import ECL as SERVER_PORTS
from robotBasics.constants.misc import QEC as MISC_CONST
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def request_cb(data, arg):
    """
        Callback function for quadratic encoder controler:
        Triggered when a request is received.
        Update the quadratic encoder value from the qe fl module
        if needed and responds to the request with the computed
        travelled distance.
    """

    if time - arg["last_update"] > MISC_CONST["update_freq"]:
        
    #Responding the request with the obstacle presence status
    arg["connection"].send_to_clients([int(ATCON.readU16(0))])


###########################################################################
#                      SERVERS SET UP AND SETTINGS :                      #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["qec"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send medium integer unsigned (number of ticks)
SERVER.set_sending_datagram(['FLOAT'])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : SERVER,
    "last_update": 0
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(request_cb, ARGUMENTS)
