"""
    AIN.py
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

class ADC:
    """
        GPIO class
    """

    def setup():
        pass

    def read(pin):
        value =  random.randrange(0, 20, 1)/10
        return value

    def pin_association(pin, name):
        PIN_ASSOC[pin] = name

    def setup_behavior(mode):
        if mode.upper() == 'PRINT':
            BEHAVIOR["print_result"] = True
