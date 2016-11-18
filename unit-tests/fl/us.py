"""
    us.py
    TEST SCRIPT !
    Reads and print the us status through the attiny45

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time

#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
import Adafruit_BBIO.GPIO as GPIO

####################################################
#               Simulator setup                    #
####################################################

GPIO.pin_association(GPIODEF.SONAR['obstacle'], 'obstacle detection')
GPIO.setup_behavior('print')


GPIO.setup(GPIODEF.SONAR['obstacle'], GPIO.IN)
while True:
    if GPIO.input(GPIODEF.SONAR['obstacle']):
        print("Obstacle detected !")
    else:
        print("The path is clear")
    time.sleep(0.5)