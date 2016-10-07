"""
    pb.py
    Handles reset button events
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
def ButtonPressed():

def ButtonReleased():


GPIO.add_event_detect(RB.gpiodef.RESET, GPIO.FALLING, callback=ButtonPressed)
GPIO.add_event_detect(RB.gpiodef.RESET, GPIO.FALLING, callback=ButtonReleased)