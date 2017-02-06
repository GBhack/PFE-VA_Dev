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
import random
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
def rotateList(data, rotation):
    if rotation > 0:
        for i in range(rotation):
            value = data.pop(0)
            data.append(value)
    elif rotation < 0:
        for i in range(rotation):
            value = data.pop()
            data.insert(0, value)
    return data

def removeSideCoeffs(data, sideLength):
    lastIndex = len(data) - 1
    if sideLength >= 0 and sideLength <= lastIndex/2:
        for i in range(sideLength - 1):
            data[i] = 0
            data[lastIndex - i] = 0
    return data


def readBarCode(sensorState):
    valueToReturn = '0'
    global barCode
    global timeBetweenCodes
    global startTimer

    if not barCode[0][0] and not barCode[0][1]: # No barcode read
        if sensorState[0] == 1 and sensorState[1] == 0: #Bar code on the left
            barCode[0][0] = True
        else:
            barCode[0][0] = False

        if sensorState[6] == 1 and sensorState[5] == 0: #Bar code on the right
            
            barCode[0][1] = True
        else:
            barCode[0][1] = False

    if barCode[0][0] or barCode[0][1]: #We already read a barcode and will wait a bit to avoid missing a white square
        if not timeBetweenCodes:
            startTimer = time.time()
        if sensorState[0] == 0 and previousSensorState[0] == 1 or sensorState[6] == 0 and previousSensorState[6] == 1: #We went through the first line of bar code
            timeBetweenCodes = time.time() - startTimer
            time.sleep(timeBetweenCodes * 1.5)
            if sensorState[0] and  sensorState[6]:
                barCode[1][0] = True
                barCode[1][1] = True
                time.sleep(timeBetweenCodes * 0.6)
            
            # At this point, we have read the whole barcode
            # 'Left Right Straight'
            timeBetweenCodes = 0
            if barCode[0][0] and not barCode[0][1]:
                valueToReturn = ['right', 'straight']
            elif not barCode[0][0] and barCode[0][1]:
                valueToReturn = ['left', 'straight']
            elif barCode[0][0] and barCode[0][1]:
                valueToReturn = ['right', 'left', 'straight']
            elif barCode[0][0] and barCode[0][1] and barCode[1][0] and barCode[1][1]:
                valueToReturn = ['right', 'left']

            barCode = [[False, False],[False, False]]           
    return valueToReturn

def adjust_steering(sensorState, steeringClient):

    global coeffs
    global turnProcess
    global direction

    lineRead = 0
    numberOfOnes = 0
    coeffsSum = 0

    numberOfOnes = sum(sensorState)
    if numberOfOnes == 0:
        for i in range(1,5):
            if previousSensorState[i]:
                coeffsSum = coeffsSum + coeffs[i]
        if coeffsSum < 0:
            lineRead = -100
        else:
            lineRead = 100
    else:
        if turnProcess == -1:
            whereCanWeGo = readBarCode(sensorState) #Binary word (str) : right - left - straight
            if not whereCanWeGo == '0':
                direction = random.choice(whereCanWeGo)
                print('-------------------------------' + direction)
                turnProcess = 0
            else:
                coeffs = DEFAULT_COEFFS

        elif turnProcess == 0: #Waiting before left and/or right sensors get mad
            print('****************TURN PROCESS ' + str(turnProcess))
            if direction == 'right': #waiting before left sensors trigger before disabling them
                if sensorState[:2] != [0,0]:
                    coeffs = [0,0,0,10,40,80,100]
                    turnProcess = 2

            elif direction == 'straight' or direction == 'left': #waiting before any of the side sensors trigger
                if sensorState[:2] != [0,0] or sensorState[-2:] != [0,0]: #coeffs = [-100,-80,-40,-10,0,0,0]
                    coeffs = [0,0,-30,0,30,0,0]
                    turnProcess = 1

        elif turnProcess == 1:
            print('****************TURN PROCESS ' + str(turnProcess))
            if direction == 'straight' or direction == 'left':
                if sensorState[:2] == [0,0] and sensorState[-2:] == [0,0]:
                    turnProcess = 2

        elif turnProcess == 2:
            print('****************TURN PROCESS ' + str(turnProcess))
            if direction == 'right':
                if sensorState[:2] == [0,0]:
                    coeffs = DEFAULT_COEFFS
                    turnProcess = -1
            elif direction == 'left':
                if sensorState[:2] != [0,0]:
                    coeffs = [-100,-80,-40,-10,0,0,0]
                    turnProcess = 3
            elif direction == 'straight':
                if sensorState[:2] != [0,0] or sensorState[-2:] != [0,0]:
                    turnProcess = 3

        elif turnProcess == 3:
            print('****************TURN PROCESS ' + str(turnProcess))
            if direction == 'left':
                if sensorState[-2:] == [0,0]:
                    coeffs = [0,0,-30,0,30,0,0]
                    turnProcess = 4
            elif direction == 'straight':
                if sensorState[:2] != [0,0] or sensorState[-2:] != [0,0]:
                    coeffs = DEFAULT_COEFFS
                    turnProcess = -1

        elif turnProcess == 4:   
            print('****************TURN PROCESS ' + str(turnProcess)) 
            if direction == 'left':
                if sensorState[:2] != [0,0] and sensorState[-2:] != [0,0]:
                    turnProcess = 5

        elif turnProcess == 5:
            print('****************TURN PROCESS ' + str(turnProcess))
            if direction == 'left':
                if sensorState[:2] == [0,0] and sensorState[-2:] == [0,0]:
                    coeffs = DEFAULT_COEFFS
                    turnProcess = -1


        for i in range(1,5):
            if sensorState[i]:
                coeffsSum = coeffsSum + coeffs[i]

        lineRead = coeffsSum/numberOfOnes
   
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
previousSteering = 0

startTimer = 0
timeBetweenCodes = 0
barCode = [[False, False],[False, False]]

DEFAULT_COEFFS = [0, -100, -80, 0, 80, 100, 0]
coeffs = DEFAULT_COEFFS

direction = ''
turnProcess = -1 #-1 = undefined (no barCode crossed), 0 = before, 1 = just before, 2 = big bordel, 3 = just after, 4 = fully after

while STEERING_CLIENT.connected and SENSOR_CLIENT.connected:
    newSensorState = SENSOR_CLIENT.request()[0]
    if newSensorState != previousSensorState:
        adjust_steering(newSensorState, STEERING_CLIENT)
        previousSensorState = newSensorState

