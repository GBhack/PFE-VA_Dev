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
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import QE as QE_CS
from robotBasics.constants.connectionSettings import QEC as QEC_CS
from robotBasics.constants.misc import QEC as MISC_CONST
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
LOGGER = robotLogger("ECL > qec", ROBOT_ROOT+'logs/ecl/')

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
        arg["distance"] = 0.0055*arg["client"].request()[0]

    #Responding the request with the obstacle presence status
    arg["server"].send_to_clients([arg["distance"]])


###########################################################################
#                   CONNECTIONS SET UP AND SETTINGS :                     #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(QEC_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

### CLIENTS CONNECTION :

#Creating the connection object
CLIENT = Client(QE_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CLIENT.close)

#Opening the connection
CLIENT.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "server" : SERVER,
    "client": CLIENT,
    "last_update": 0,
    "distance": 0
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(request_cb, ARGUMENTS)
