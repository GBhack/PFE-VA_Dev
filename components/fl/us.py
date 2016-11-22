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

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import SONAR as SONAR_GPIO
from robotBasics.constants.ports import FL as SERVER_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
##Adafruit_BBIO:
import Adafruit_BBIO.GPIO as GPIO

"""
###########################################################################
#                           Simulator setup                               #
###########################################################################

GPIO.pin_association(SONAR_GPIO["obstacle"], 'obstacle detection status')
GPIO.setup_behavior('print')
"""

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
    arg["connection"].send_to_clients([obstacleDetected])


###########################################################################
#                     SERVER SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["us"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send booleans (obstacle detection status)
SERVER.set_sending_datagram(['BOOL'])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : SERVER
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(obstacle_detection_cb, ARGUMENTS)
