"""
    gpiodef.py
    BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Engines-related I/O :
ENGINES = {
    "left": {
        "PWM":        "P9_16", # MARRON
        "forward":    "P9_23", # BLANC
        "backward":   "P9_25"  # VERT
    },
    "right": {
        "PWM":        "P9_14", # MARRON
        "forward":    "P9_29",
        "backward":   "P9_31"
    }
}

#LEDs-related I/O :
# !!!!!! A CHANGER  !!!!!!!!
LEDS = {
    "left": "P8_33",    #violet
    "right": "P8_27",   #bleu
    "stop": "P8_29",
    "status": "P8_31"
}

#Sonar-related I/O :
SONAR = {
    "trigger": "P8_8",
    "echo": "P8_10",
    "obstacle": "P8_13",
}

OS = ["AIN4", "AIN6", "AIN3", "AIN2", "AIN1", "AIN0", "AIN5"]

#Reset pushbutton
RESET = "P8_7"
