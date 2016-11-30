"""
    us.py
    Functional Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    When gets a request, responds with the obstacle detection
    state (read through the Attiny)

"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import SONAR as SONAR_GPIO
from robotBasics.constants.connectionSettings import US as US_CS
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger
##Adafruit_BBIO:
import Adafruit_BBIO.GPIO as GPIO

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

    #Simulator setup
    GPIO.pin_association(SONAR_GPIO["obstacle"], 'obstacle detection status')
    GPIO.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > us", ROBOT_ROOT+'logs/fl/')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
GPIO.setup(SONAR_GPIO["obstacle"], GPIO.IN)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def obstacle_detection_cb(data, arg):
    """
        Callback function for obstacle detection :
        Triggered when a request is received.
        Reads the obstacle presence state and responds
        to the request.
    """
    #By default, we consider that there is no obstacle
    obstacleDetected = False

    #If the Atitiny's obstacle presence pin is high (obstacle
    #detected), changes obstacleDetected to True
    if GPIO.input(SONAR_GPIO["obstacle"]):
        LOGGER.info('Obstacle detected.')
        obstacleDetected = True

    #Responding the request with the obstacle presence status
    arg["connection"].send([obstacleDetected])


###########################################################################
#                     SERVER SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(US_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "connection" : SERVER
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(obstacle_detection_cb, ARGUMENTS)
