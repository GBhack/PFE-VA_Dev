"""
    qe.py
    TEST SCRIPT !
    Reads and print the quadratic encoder status through the attiny45

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time


#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
from Adafruit_I2C import Adafruit_I2C
 
i2c = Adafruit_I2C(0x04,2)

while True:
    print('QE value : '+str(i2c.readU16(0)))
    time.sleep(0.5)