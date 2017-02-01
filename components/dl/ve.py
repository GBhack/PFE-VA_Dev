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
from robotBasics.constants.connectionSettings import LEDC as LEDC_CS
from robotBasics.constants.gpiodef import LEDS_ID as LEDS_ID
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
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()
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
    args["velocity_server"].send([True])
    args["velocity_state"]["busy"] = False

def brake_light_switch(state, client):
    print('LED STATE : ', state)
    print([LEDS_ID["STOP"], state])
    client.send([[LEDS_ID["STOP"], int(state)]])

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :


VELOCITY_CLIENT = Client(VSC_CS["velocity"], LOGGER)

#Opening the connection
VELOCITY_CLIENT.connect()

LEDS_CLIENT = Client(LEDC_CS, LOGGER)

#Opening the connection
LEDS_CLIENT.connect()
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
previousBrakeLightCommand = False

while VELOCITY_SERVER.connected:
    brakeLightCommand = False
    if VELOCITY_STATE["oa_brake"]:
        print("Brake")
        desiredVelocity = 0
    else:
        desiredVelocity = int(VELOCITY_STATE["desiredVelocity"])
    brakeLightCommand = (desiredVelocity < int(VELOCITY_STATE["actualVelocity"]) or desiredVelocity == 0)
    if VELOCITY_STATE["actualVelocity"] != desiredVelocity:
        VELOCITY_CLIENT.send([desiredVelocity])
        VELOCITY_STATE["actualVelocity"] = VELOCITY_CLIENT.receive()[0]
    if previousBrakeLightCommand != brakeLightCommand:
        brake_light_switch(brakeLightCommand, LEDS_CLIENT)
        previousBrakeLightCommand = brakeLightCommand

    #print('Required velocity : ' + str(desiredVelocity))
    #print('Actual velocity : ' + str(VELOCITY_STATE["actualVelocity"]))
    time.sleep(0.25)
