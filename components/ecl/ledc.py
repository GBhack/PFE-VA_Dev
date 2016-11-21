"""
    ledc.py
    LEDs Controller
    Manage the LED's state
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-


###Standard imports :
import atexit

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
    print("hey")
    print(data)
    if args["LEDs_state"][data[0][0]] != bool(data[0][1]):
        args["LEDs_state"][data[0][0]] = bool(data[0][1])
        args["client"].send_data([args["LEDs_state"]])
        args["server"].send_to_clients([args["client"].receive_data()[0]])
    else:
        args["server"].send_to_clients([True])

#### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = SOCKETS.tcp.Client.Client(CLIENTS_PORTS["led"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#We'll send booleans (request)
CLIENT.set_sending_datagram([['BITS', [1, 1, 1, 1]]])

#We'll receive booleans (operation status)
CLIENT.set_receiving_datagram(['BOOL'])

#Opening the connection
CLIENT.set_up_connection()


#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["ledc"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll receive three bits (LED ID on 2 bits + state on 1 bit)
SERVER.set_receiving_datagram([['BITS', [2, 1]]])

#We'll send booleans (operation status)
SERVER.set_sending_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()


#Argument to be passed to the steering callback method
ARGUMENTS = {
    "server": SERVER,
    "client": CLIENT,
    "LEDs_state": [False, False, False, False]
}

#Waiting for requests and redirecting them to the callback methods
SERVER.listen_to_clients(request_cb, ARGUMENTS)
