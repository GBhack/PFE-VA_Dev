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

THRESHOLD = 1.7

def readSingleSensor(sensor):
    return ADC.read(sensor) > THRESHOLD

def readSensorArray():
    array = [0, 0, 0, 0, 0, 0, 0]
    for i in range(7):
        array[i]=int(readSingleSensor(GPIODEF.OS[i]))
    return array


ADC.setup()

while True:
    print(readSensorArray())
    time.sleep(0.5)