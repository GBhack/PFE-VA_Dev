"""
    led.py
    TEST SCRIPT !
    Changes the LEDs status status

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time


#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
import Adafruit_BBIO.GPIO as GPIO

"""
####################################################
#               Simulator setup                    #
####################################################

GPIO.pin_association(GPIODEF.LEDS[0], 'left blinker')
GPIO.pin_association(GPIODEF.LEDS[1], 'right blinker')
GPIO.pin_association(GPIODEF.LEDS[2], 'stop light')
GPIO.pin_association(GPIODEF.LEDS[3], 'status LED')
GPIO.setup_behavior('print')
"""

####################################################
#                     I/O setup                    #
####################################################

GPIO.setup(GPIODEF.LEDS[0], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS[1], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS[2], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS[3], GPIO.OUT)

GPIO.output(GPIODEF.LEDS[0], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS[1], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS[2], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS[3], GPIO.HIGH)

####################################################
#                   Main script                    #
####################################################

while True:
    GPIO.output(GPIODEF.LEDS[0], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS[1], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS[2], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS[3], GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIODEF.LEDS[0], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS[1], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS[2], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS[3], GPIO.LOW)
    time.sleep(0.5)
