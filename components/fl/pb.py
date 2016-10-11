"""
    pb.py
    Handles reset button events
    If button pressed  : send TRUE
    If button released : send FALSE
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO

def button_pressed_event():
    """
        Handles the pressed button event
    """
    UDP.send_to_clients([True])

def button_released_event():
    """
        Handles the released button event
    """
    UDP.send_to_clients([False])

SOCKETS = RB.sockets

UDP = SOCKETS.udp.Server.Server(RB.constants.ports.FL["pb"])
UDP.set_sending_datagram(["BOOL"])

GPIO.add_event_detect(RB.constants.gpiodef.RESET, GPIO.FALLING, callback=button_pressed_event)
GPIO.add_event_detect(RB.constants.gpiodef.RESET, GPIO.FALLING, callback=button_released_event)
