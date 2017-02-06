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

    coeffs = [-100,-70,-50,0,50,70,100]
    lineRead = 0
    numberOfOnes = 0
    coeffsSum = 0

    numberOfOnes = sum(sensorState)
    if numberOfOnes == 0:
        for i in range(len(sensorState)):
            if previousSensorState[i]:
                coeffsSum = coeffsSum + coeffs[i]
        if coeffsSum < 0:
            lineRead = -100
        else:
            lineRead = 100
    else:
        for i in range(len(sensorState)):
            if sensorState[i]:
                coeffsSum = coeffsSum + coeffs[i]

        lineRead = coeffsSum/numberOfOnes
    
    # if abs(lineRead - previousSteering) > 50 : #We either read a barcode, or we are at an intersection
    # 	if abs(lineRead) < 30: #We are on a straight line, in the middle (normal situation)
    # 		if sensorState[0] == 1 and sensorState[1] == 0: #Bar code on the left


    steering = lineRead
    steeringClient.send([int(steering)])

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
previousSteering = 50

while STEERING_CLIENT.connected and SENSOR_CLIENT.connected:
    newSensorState = SENSOR_CLIENT.request()[0]
    if newSensorState != previousSensorState:
        adjust_steering(newSensorState, STEERING_CLIENT)
        previousSensorState = newSensorState

