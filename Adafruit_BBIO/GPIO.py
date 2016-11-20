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

class GPIO:
    """
        GPIO class
    """
    OUT = False
    IN = True
    LOW = False
    HIGH = True

    def setup(pin, mode):
        detail = ''
        if pin in PIN_ASSOC:
            detail = ' ('+PIN_ASSOC[pin]+')'
        if mode:
            message = 'PIN '+pin+detail+' setup as INPUT'
        else:
            message = 'PIN '+pin+detail+' setup as OUTPUT'
        
        LOGGER.debug(message)
        if BEHAVIOR["print_result"]:
            print(message)
        #LOGGER.error('Message d\'erreur 1')

    def output(pin, state):
        detail = ''
        if pin in PIN_ASSOC:
            detail = ' ('+PIN_ASSOC[pin]+')'
        if state:
            message = 'PIN '+pin+detail+'\'s state changed to HIGH'
        else:
            message = 'PIN '+pin+detail+'\'s state changed to LOW'
        LOGGER.debug(message)
        if BEHAVIOR["print_result"]:
            print(message)

    def input(pin):
        return random.randrange(0, 2, 1)

    def pin_association(pin, name):
        PIN_ASSOC[pin] = name

    def setup_behavior(mode):
        if mode.upper() == 'PRINT':
            BEHAVIOR["print_result"] = True
