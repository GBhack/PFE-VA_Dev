"""
    vp.py
    Decision Level module : Velocity Planning
    Executes the velocity plan while handeling emergency brake
    if requested by the oa module.
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import time
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import VE as VE_CS
from robotBasics.constants.connectionSettings import PBC as PBC_CS
#Classes & Methods:
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
LOGGER = robotLogger("DL > vp", ROBOT_ROOT+'logs/dl/')

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################


###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

VELOCITY_CLIENT = Client(VE_CS["velocity"], LOGGER)

#Opening the connection
VELOCITY_CLIENT.connect()

PBC_CLIENT = Client(PBC_CS, LOGGER)

#Opening the connection
PBC_CLIENT.connect()

#### CALLBACKS' ARGUMENTS SETUP:

###########################################################################
#                               RUNNING :                                 #
###########################################################################

RUNNING = False

while VELOCITY_CLIENT.connected and PBC_CLIENT.connected:
    if PBC_CLIENT.request()[0]:
        RUNNING = not RUNNING
        if RUNNING:
            VELOCITY_CLIENT.send([40])
        else:
            VELOCITY_CLIENT.send([0])
    time.sleep(0.25)
