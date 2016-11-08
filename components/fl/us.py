"""
    us.py
    Functional Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    When gets a request, responds with the obstacle detection
    state (read through the Atitiny)

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import atexit
import time


#Specific imports :
from robotBasics import constants as CONSTANTS
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
import Adafruit_BBIO.GPIO as GPIO


###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
GPIO.setup(CONSTANTS.gpiodef.SONAR["echo"], GPIO.IN)

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
    if GPIO.input(CONSTANTS.gpiodef.SONAR["echo"]):
        LOGGER.info('Obstacle detected.')
        obstacleDetected = True

    #Responding the request with the obstacle presence status
    arg["connection"].send_to_clients([obstacleDetected])


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.FL["us"])
print(CONSTANTS.ports.FL["us"])

#We'll send bool
SERVER.set_sending_datagram(['BOOL'])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection(10)

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : SERVER
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(obstacle_detection_cb, ARGUMENTS)

atexit.register(SERVER.close)
