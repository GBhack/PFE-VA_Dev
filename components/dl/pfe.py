"""
    pfe.py
    Decision Level module : Path-Following Executor
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
from robotBasics.constants.connectionSettings import OS as OS_CS
from robotBasics.constants.connectionSettings import VSC as VSC_CS
#from robotBasics.constants.connectionSettings import LEDC as LEDC_CS
#from robotBasics.constants.misc import LEDS_ID as LEDS_ID
#Classes & Methods:
#from robotBasics.sockets.tcp.Server import Server as Server
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
LOGGER = robotLogger("DL > pfe", ROBOT_ROOT+'logs/dl/')

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def adjust_steering(sensorState, steeringClient):
    steering = 0
    if sensorState[4]:
        if sensorState[3]:
            steering = 10
        elif sensorState[5]:
            steering = -10
    else:
        if sensorState[3]:
            steering = 20
        elif sensorState[5]:
            steering = -20
        if sensorState[2]:
            steering = 40
        elif sensorState[6]:
            steering = -40
    steeringClient.send([steering])
###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

STEERING_CLIENT = Client(VSC_CS["steering"], LOGGER)

#Opening the connection
STEERING_CLIENT.connect()

SENSOR_CLIENT = Client(OS_CS, LOGGER)

#Opening the connection
SENSOR_CLIENT.connect()

previousSensorState = [0, 0, 0, 0, 0, 0, 0]

while STEERING_CLIENT.connected and SENSOR_CLIENT.connected:
    newSensorState = SENSOR_CLIENT.request()[0]
    if newSensorState != previousSensorState:
        adjust_steering(newSensorState, STEERING_CLIENT)
        previousSensorState = newSensorState

