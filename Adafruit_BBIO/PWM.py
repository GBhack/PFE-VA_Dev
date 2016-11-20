"""
    GPIO.py
    Adafruit_BBIO GPIO simulator
    Designed to simulate the official Adafruit library on any computer.
    Reads inputs from a file and logs the outputs in a file.

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
import random

from .logger import logger as LOGGER

PIN_ASSOC = {}
BEHAVIOR = {"print_result" : False}

class PWM:
    """
        GPIO class
    """

    def start(pin, duty, freq = 1000):
        detail = ''
        if pin in PIN_ASSOC:
            detail = ' ('+PIN_ASSOC[pin]+')'

        message = 'PWM started on PIN '+pin+detail+' with a duty cycle of '+str(duty)
        
        LOGGER.debug(message)
        if BEHAVIOR["print_result"]:
            print(message)
        #LOGGER.error('Message d\'erreur 1')

    def set_duty_cycle(pin, duty):
        detail = ''
        if pin in PIN_ASSOC:
            detail = ' ('+PIN_ASSOC[pin]+')'

        message = 'PWM changed to '+str(duty)+' on PIN '+pin+detail

        LOGGER.debug(message)
        if BEHAVIOR["print_result"]:
            print(message)

    def pin_association(pin, name):
        PIN_ASSOC[pin] = name

    def setup_behavior(mode):
        if mode.upper() == 'PRINT':
            BEHAVIOR["print_result"] = True
