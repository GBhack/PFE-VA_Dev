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

def button_event():
    """
        Handles the reset button event
    """
    UDP.send_to_clients(GPIO.input(RB.constants.gpiodef.RESET))

SOCKETS = RB.sockets
###########DEFINE GPIO AS INPUT
UDP = SOCKETS.udp.Server.Server(RB.constants.ports.FL["pb"])
UDP.set_sending_datagram(["BOOL"])

GPIO.add_edge_callback(RB.constants.gpiodef.RESET, button_event)
