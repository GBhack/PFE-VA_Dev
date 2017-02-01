"""
    abort.py
    Abort all operations
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
#import atexit
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants import gpiodef as GPIODEF
from robotBasics.constants.gpiodef import LEDS as LEDS_GPIO
from robotBasics.constants.gpiodef import LEDS_PINS as LEDS_PINS
#Classes & Methods:
from robotBasics.logger import robotLogger

###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'
    import Adafruit_BBIO.GPIO as GPIO
    import Adafruit_BBIO.PWM as PWM
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()

    import Adafruit_BBIO_SIM.GPIO as GPIO
    import Adafruit_BBIO.PWM as PWM

    #Simulator setup
    PWM.pin_association(GPIODEF.ENGINES["left"]["PWM"], 'left motor\'s PWM')
    PWM.pin_association(GPIODEF.ENGINES["right"]["PWM"], 'right motor\'s PWM')
    GPIO.pin_association(GPIODEF.ENGINES["left"]["forward"], 'left motor\'s forward pin')
    GPIO.pin_association(GPIODEF.ENGINES["right"]["forward"], 'right motor\'s forward pin')
    GPIO.pin_association(GPIODEF.ENGINES["left"]["backward"], 'left motor\'s backward pin')
    GPIO.pin_association(GPIODEF.ENGINES["right"]["backward"], 'right motor\'s backward pin')
    GPIO.setup_behavior('print')
    PWM.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("abort", ROBOT_ROOT+'logs/')

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

LOGGER.debug('Aborting');

MOTOR_LEFT = GPIODEF.ENGINES["left"]
MOTOR_RIGHT = GPIODEF.ENGINES["right"]

LOGGER.debug('Stopping motors');
#Start PWM with a 0% duty cycle
PWM.start(MOTOR_LEFT["PWM"], 0)
PWM.start(MOTOR_RIGHT["PWM"], 0)


#Declare motor enabling pins as outputs
GPIO.setup(MOTOR_LEFT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_LEFT["backward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["backward"], GPIO.OUT)

#Set enabeling pins to LOW
########### NOTE ############
# To go forward  : set forward  pin to 1 and backward pin to 0
# To go backward : set backward pin to 1 and forward  pin to 0
GPIO.output(MOTOR_LEFT["forward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["forward"], GPIO.LOW)
GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)

LOGGER.debug('Turning LEDs down');
for LED in LEDS_PINS:
    #Declare motor enabling pins as outputs
    GPIO.setup(LED, GPIO.OUT)
    #Set pins to HIGH (LEDs off)
    GPIO.output(LED, GPIO.HIGH)

LOGGER.debug('Abortion successfull');
