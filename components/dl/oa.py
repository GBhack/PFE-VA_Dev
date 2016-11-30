"""
    oa.py
    Decision Level module : Obstacle Avoidance
    Periodically checks the frontal distance and brakes if necesssary
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
from robotBasics.constants.connectionSettings import USC as USC_CS
#Classes & Methods:
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
    ROBOT_ROOT = open(path.expanduser('~/.robotConf'), 'r').read().strip().close()
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("DL > oa", ROBOT_ROOT+'logs/dl/')

UPDATE_RATE = 0.1
MINIMAL_DISTANCE = 0.08

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the Get Frontal Distance module's client
UC_CLIENT = Client(USC_CS, LOGGER)

#Opening the connection
UC_CLIENT.connect()

#Creating the Velocity/Steering regulator module's client object
VE_CLIENT = Client(VE_CS["oa"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VE_CLIENT.close)

#Opening the connection
VE_CLIENT.connect()

###########################################################################
#                               RUNNING :                                 #
###########################################################################

alive = True
while VE_CLIENT.connected and UC_CLIENT.connected:
    result = UC_CLIENT.request()
    print('Request result : ', result)
    VE_CLIENT.send([UC_CLIENT.request()])
    time.sleep(UPDATE_RATE)
