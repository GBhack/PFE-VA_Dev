"""
    ve.py
    Decision Level module : Velocity Executor
    Executes the velocity plan while handeling emergency brake
    if requested by the oa module.
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
from robotBasics.constants.connectionSettings import VE as VE_CS
from robotBasics.constants.connectionSettings import VSC as VSC_CS
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
LOGGER = robotLogger("DL > ve", ROBOT_ROOT+'logs/dl/')

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def oa_handling_cb(data, args):
    if data[0]:
        while  args["velocity_state"]["busy"]:
            time.sleep(0.0001)
        args["velocity_state"]["busy"] = True
        args["velocity_state"]["oa_brake"] = True
        args["velocity_client"].send([0])
        _ = args["velocity_client"].receive()
        args["velocity_state"]["busy"] = False
    else:
        args["velocity_state"]["oa_brake"] = False

def velocity_handling_cb(data, args):

    while  args["velocity_state"]["busy"]:
        time.sleep(0.001)
    args["velocity_state"]["busy"] = True
    print('Velocity received : ', int(data[0]))
    args["velocity_state"]["desiredVelocity"] = int(data[0])
    args["velocity_server"].send_to_clients([True])
    args["velocity_state"]["busy"] = False

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#
VELOCITY_CLIENT = Client(VSC_CS["velocity"], LOGGER)

#Opening the connection
VELOCITY_CLIENT.connect()

#### SERVER CONNECTION :

#Creating the TCP instances
OA_SERVER = Server(VE_CS["oa"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(OA_SERVER.close)

#Opening the connection
OA_SERVER.connect()

## Velocity Server :

#Creating the TCP instance
VELOCITY_SERVER = Server(VE_CS["velocity"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VELOCITY_SERVER.close)

#Opening the connection
VELOCITY_SERVER.connect()

#### CALLBACKS' ARGUMENTS SETUP:

VELOCITY_STATE = {
    "busy": False,
    "oa_brake": False,
    "actualVelocity": 0,
    "desiredVelocity": 0
}

OA_ARGUMENTS = {
    "velocity_state": VELOCITY_STATE,
    "velocity_client": VELOCITY_CLIENT
}

VELOCITY_ARGUMENTS = {
    "velocity_state": VELOCITY_STATE,
    "velocity_server": VELOCITY_SERVER
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and redirecting them to the callback methods
VELOCITY_SERVER.listen_to_clients(velocity_handling_cb, VELOCITY_ARGUMENTS)
OA_SERVER.listen_to_clients(oa_handling_cb, OA_ARGUMENTS)

alive = True

while VELOCITY_SERVER.connected:
    if VELOCITY_STATE["oa_brake"]:
        print("Brake")
        desiredVelocity = 0
    else:
        desiredVelocity = int(VELOCITY_STATE["desiredVelocity"])
    if VELOCITY_STATE["actualVelocity"] != desiredVelocity:
        VELOCITY_CLIENT.send([desiredVelocity])
        VELOCITY_STATE["actualVelocity"] = VELOCITY_CLIENT.receive()
    print('Required velocity : ' + str(desiredVelocity))
    print('Actual velocity : ' + str(VELOCITY_STATE["actualVelocity"]))
    time.sleep(0.25)
