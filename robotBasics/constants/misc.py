"""
    constants.py
    Miscellaneous constants
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

from logging import DEBUG
from .gpiodef import LEDS as LEDS_GPIO

#Sockets-related constants
SOCKETS = {
    "connectionTimeout": 20,
    "listeningTimeOut": 120,
    "frequency": 0.02
}

PHYSICAL = {
    "axle": 0.15
}

LOGGING = {
    "level": DEBUG
}

OS = {
    "threshold": 1.2
}

QEC = {
    "update_freq": 0.25
}

IP = {
	"max_retry" : 5
}
