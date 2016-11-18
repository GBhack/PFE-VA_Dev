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

####################################################
#               Simulator setup                    #
####################################################

GPIO.pin_association(GPIODEF.LEDS["left"], 'left blinker')
GPIO.pin_association(GPIODEF.LEDS["right"], 'right blinker')
GPIO.pin_association(GPIODEF.LEDS["stop"], 'stop light')
GPIO.pin_association(GPIODEF.LEDS["status"], 'status LED')
GPIO.setup_behavior('print')

####################################################
#                     I/O setup                    #
####################################################

GPIO.setup(GPIODEF.LEDS["left"], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS["right"], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS["stop"], GPIO.OUT)
GPIO.setup(GPIODEF.LEDS["status"], GPIO.OUT)

GPIO.output(GPIODEF.LEDS["left"], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS["right"], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS["stop"], GPIO.HIGH)
GPIO.output(GPIODEF.LEDS["status"], GPIO.HIGH)

####################################################
#                   Main script                    #
####################################################

while True:
    GPIO.output(GPIODEF.LEDS["left"], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS["right"], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS["stop"], GPIO.HIGH)
    GPIO.output(GPIODEF.LEDS["status"], GPIO.HIGH)
    time.sleep(0.5)
    GPIO.output(GPIODEF.LEDS["left"], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS["right"], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS["stop"], GPIO.LOW)
    GPIO.output(GPIODEF.LEDS["status"], GPIO.LOW)
    time.sleep(0.5)
