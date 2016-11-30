"""
    Adafruit_I2C.py
    Adafruit_BBIO I2C simulator
    Designed to simulate the official Adafruit library on any computer.
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
import random

from .logger import logger as LOGGER

PIN_ASSOC = {}
COUNTER = {"state": -1}
BEHAVIOR = {"print_result" : False}

class IIC:
    """
        GPIO class
    """
    def __init__(self, address, subaddress):
        pass

    def readU16(self, val):
        COUNTER["state"] += random.randrange(0, 12, 1)
        return COUNTER["state"]

    def setup_behavior(self, mode):
        if mode.upper() == 'PRINT':
            BEHAVIOR["print_result"] = True
