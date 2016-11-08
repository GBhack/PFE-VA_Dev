"""
    os.py
    TEST SCRIPT !
    Reads and print the optical sensor status

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time


#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
import Adafruit_BBIO.ADC as ADC
 
ADC.setup()

while True:
    value = ADC.read("P9_33")
    time.sleep(0.5)