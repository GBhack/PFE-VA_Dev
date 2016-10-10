"""
    pb.py
    Handles reset button events
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO

def button_pressed_event():
    """
        Handles the pressed button event
    """

def button_released_event():
    """
        Handles the released button event
    """
    pass

GPIO.add_event_detect(RB.constants.gpiodef.RESET, GPIO.FALLING, callback=button_pressed_event)
GPIO.add_event_detect(RB.constants.gpiodef.RESET, GPIO.FALLING, callback=button_released_event)
