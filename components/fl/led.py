"""
    led.py
    Waits for a description of the desired state for the two LEDs,
    apply the appropriate configuration on the GPIO and responds with
    a notification when the request has been fulfilled.
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import LEDS as LEDS
from robotBasics.constants.ports import FL as SERVER_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
##Adafruit_BBIO:
import Adafruit_BBIO.GPIO as GPIO

###########################################################################
#                             Simulator setup                             #
###########################################################################

GPIO.pin_association(LEDS[0], 'left blinker')
GPIO.pin_association(LEDS[1], 'right blinker')
GPIO.pin_association(LEDS[2], 'brake light')
GPIO.setup_behavior('print')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#Declare motor enabling pins as outputs
GPIO.setup(LEDS[0], GPIO.OUT)
GPIO.setup(LEDS[1], GPIO.OUT)
GPIO.setup(LEDS[2], GPIO.OUT)

#Set enabeling pins to LOW
########### NOTE ############
GPIO.output(LEDS[0], GPIO.LOW)
GPIO.output(LEDS[1], GPIO.LOW)
GPIO.output(LEDS[2], GPIO.LOW)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def set_leds_cb(data, args):
    """
        Callback function motor controlling:
        When instructions are updated through a request to the
        server, deduces and apply the corresponding motor configuration
    """
    for i, led in enumerate(LEDS):
        if data[0][i]:
            GPIO.output(led, GPIO.HIGH)
        else:
            GPIO.output(led, GPIO.LOW)
        args["connection"].send_to_clients([True])

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the TCP instances
LEDS_SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["led"], LOGGER)

#Registering the close method to be executed at exit (clean deconnection)
atexit.register(LEDS_SERVER.close)

#We'll send booleans (success of the operation)
LEDS_SERVER.set_sending_datagram(['BOOL'])

#We'll receive an array of bits (LEDs state description)
LEDS_SERVER.set_receiving_datagram([['BITS', [1, 1, 1, 1]]])

#Opening the connection
LEDS_SERVER.set_up_connection(600)

#Arguments object for the callback method
#We pass the CONNECTION object so that the callback can respond to the request
ARGUMENTS = {
    "connection": LEDS_SERVER
}

#Waiting for requests and redirecting them to the callback method
LEDS_SERVER.listen_to_clients(set_leds_cb, ARGUMENTS)
