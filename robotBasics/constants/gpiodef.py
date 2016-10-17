"""
    gpiodef.py
    BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Engines-related I/O :
ENGINES = {
    "left": {
        "PWM":        "P9_16",
        "forward":    "P8_7",
        "backward":   "P8_10"
    },
    "right": {
        "PWM":        "P9_14",
        "forward":    "P8_8",
        "backward":   "P8_9"
    }
}

#LEDs-related I/O :
LEDS = {
    "left": "P8_15",
    "right": "P8_16",
    "stop": "P8_14",
    "status": "P8_17"
}

#Sonar-related I/O :
SONAR = {
    "trigger": "P8_11",
    "echo": "P8_12"
}

#Reset pushbutton
RESET = "P8_18"
