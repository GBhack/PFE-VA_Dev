"""
    pbc.py
    PushButton Controller (Mode Controller)
    Keeps track of the "mode" (ie running/pause)
    through the pushbutton.
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-


###Standard imports :
import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import PB as PB_CS
from robotBasics.constants.connectionSettings import PBC as PBC_CS
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
    ROBOT_ROOT = open(path.expanduser('~/.robotConf'), 'r').read().strip().close()
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("ECL > pbc", ROBOT_ROOT+'logs/ecl/')

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
    if args["client"].request()[0]:
        args["running"] = not args["running"]

    args["server"].send([args["running"]])

###########################################################################
#                   CONNECTIONS SET UP AND SETTINGS :                     #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = Client(PB_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#Opening the connection
CLIENT.connect()


#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(PBC_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "server": SERVER,
    "client": CLIENT,
    "running": False
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and redirecting them to the callback methods
SERVER.listen_to_clients(request_cb, ARGUMENTS)
SERVER.join_clients()
