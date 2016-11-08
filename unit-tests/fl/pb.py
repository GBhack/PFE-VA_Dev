"""
    pb.py
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

GPIO.setup(GPIODEF.RESET, GPIO.IN)

lastState = False

while True:
    if not GPIO.input(GPIODEF.RESET):
        while not GPIO.input(GPIODEF.RESET):
            pass
        print("Button pushed !")
    time.sleep(0.2)