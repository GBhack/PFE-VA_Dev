"""
    turnStatusLedOn.py
    Turns on the status LED
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.gpiodef import LEDS as LEDS_GPIO
#Classes & Methods:
from robotBasics.logger import robotLogger


###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'

    ##Adafruit_BBIO:
    import Adafruit_BBIO.GPIO as GPIO

elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()

    import Adafruit_BBIO_SIM.GPIO as GPIO

    #Simulator setup
    GPIO.pin_association(LEDS_GPIO["STATUS"][1], 'STATUS led')
    GPIO.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > led", ROBOT_ROOT+'logs/fl/')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

GPIO.setup(LEDS_GPIO["STATUS"][1], GPIO.OUT)
GPIO.output(LEDS_GPIO["STATUS"][1], GPIO.LOW)
