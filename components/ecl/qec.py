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
import time

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
        arg["client"].send_data([True])
        arg["distance"] = 0.0055*arg["client"].receive_data()[0]

    #Responding the request with the obstacle presence status
    arg["server"].send_to_clients([arg["distance"]])


###########################################################################
#                      SERVERS SET UP AND SETTINGS :                      #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["qec"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send floats (travelled distance in meters)
SERVER.set_sending_datagram(['FLOAT'])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()

### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = SOCKETS.tcp.Client.Client(CLIENTS_PORTS["qe"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#We'll send booleans (request)
CLIENT.set_sending_datagram(['BOOL'])
#We'll receive medium integer unsigned (number of ticks)
CLIENT.set_receiving_datagram(['MEDIUM_INT_UNSIGNED'])

#Opening the connection
CLIENT.set_up_connection()

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "server" : SERVER,
    "client": CLIENT,
    "last_update": 0,
    "distance": 0
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(request_cb, ARGUMENTS)
