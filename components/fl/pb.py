"""
    pb.py
    Functional Level module : PushButton manager
    Keeps track of the pushbutton's history
    Waits for a TCP request on its own port
    When gets a request, responds with True if
    the button has been pushed since last request
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import atexit
import time


#Specific imports :
from robotBasics.constants.gpiodef import RESET as RESET_GPIO
from robotBasics.constants.ports import FL as FL_PORTS
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
import Adafruit_BBIO.GPIO as GPIO

###########################################################################
#                           Simulator setup                               #
###########################################################################

GPIO.pin_association(RESET_GPIO, 'pushbutton\'s state')
GPIO.setup_behavior('print')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#GPIO setup :
GPIO.setup(RESET_GPIO, GPIO.IN)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def pb_update_cb(data, arg):
    """
        Callback function for push button status reading :
        Triggered when a request is received.
        Responds True if the button has been pushed since last
        request and then reset the button's status
    """
    #Responding the request with the button pushing status
    arg["connection"].send_to_clients([arg["state"]])
    #Reseting the button pushing status
    arg["state"] = False


###########################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
###########################################################################

#Creating the connection object
SERVER = SOCKETS.tcp.Server.Server(FL_PORTS["pb"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#We'll send bool
SERVER.set_sending_datagram(['BOOL'])

#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
SERVER.set_up_connection()

#Arguments object for the callback method
#We pass the SERVER object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : SERVER,
    "state" : False
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(pb_update_cb, ARGUMENTS)

LOOPING = True

while LOOPING:
    try:
        if not GPIO.input(RESET_GPIO):
            while not GPIO.input(RESET_GPIO):
                time.sleep(0.1)
            ARGUMENTS['state'] = True
        time.sleep(0.5)
    except:
        LOOPING = False