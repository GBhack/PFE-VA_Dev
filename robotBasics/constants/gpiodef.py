"""
    gpiodef.py
    BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Engines-related I/O :
ENGINES = {
    "left": {
        "PWM":        "P9_16", # NOIR
        "forward":    "P9_17", # BLANC
        "backward":   "P9_18"  # GRIS
    },
    "right": {
        "PWM":        "P9_14", 
        "forward":    "P9_13",
        "backward":   "P9_21"
    }
}

#LEDs-related I/O :
# !!!!!! A CHANGER  !!!!!!!!
LEDS = {
    "left": "P8_15",
    "right": "P8_16",
    "stop": "P8_14",
    "status": "P8_17"
}

#Sonar-related I/O :
SONAR = {
    "trigger": "P8_7",
    "echo": "P8_8"
}

#Reset pushbutton
RESET = "P8_18"
