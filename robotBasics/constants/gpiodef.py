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
LEDS = [
    "P8_33",    #LEFT blinker
    "P8_27",    #RIGHT blinker
    "P8_29",    #STOP light
    "P8_31"     #STATUS led
]

#Sonar-related I/O :
SONAR = {
    "trigger": "P8_8",
    "echo": "P8_10",
    "obstacle": "P8_13",
}

OS = ["AIN4", "AIN6", "AIN3", "AIN2", "AIN1", "AIN0", "AIN5"]

#Reset pushbutton
RESET = "P8_7"
