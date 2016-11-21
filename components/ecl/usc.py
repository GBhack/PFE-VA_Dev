"""
    usc.py
    Ultrasonic Sensor Controller
    Keeps the ultrasonic sensor’s data updated.
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
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER


def request_cb(data, args):
    """
        Callback function for ultrasonic sensor controler:
        Triggered when a request is received.
        Update the obstacle detection status and responds to
        the request with the updated status.
    """

    
    args["client"].send_data([True])
    time.sleep(0.05)
    args["server"].send_to_clients([args["client"].receive_data()[0]])

#### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = SOCKETS.tcp.Client.Client(CLIENTS_PORTS["us"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#We'll send booleans (request)
CLIENT.set_sending_datagram(['BOOL'])

#We'll receive booleans (obstacle detection status)
CLIENT.set_receiving_datagram(['BOOL'])

#Opening the connection
CLIENT.set_up_connection()


#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["usc"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#We'll send booleans (obstacle detection status)
SERVER.set_sending_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection(600)


#Argument to be passed to the steering callback method
ARGUMENTS = {
    "server": SERVER,
    "client": CLIENT
}

#Waiting for requests and redirecting them to the callback methods
SERVER.listen_to_clients(request_cb, ARGUMENTS)
