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
# CHANGE THE VALUES HERE !!
LEDS = {
    "LEFT" : [0, "P8_33"],
    "RIGHT" : [1, "P8_27"],
    "STOP" : [2, "P8_31"],
    "STATUS" : [3, "P8_29"]
}

LEDS_PINS = [0]*len(LEDS)
LEDS_ID = {}
LEDS_STATE = [False]*len(LEDS)

for NAME, DETAIL in LEDS.items():
    LEDS_PINS[DETAIL[0]] = DETAIL[1]
    LEDS_ID[NAME] = DETAIL[0]

#Sonar-related I/O :
SONAR = {
    "trigger": "P8_8",
    "echo": "P8_10",
    "obstacle": "P8_13",
}

OS = ["AIN4", "AIN6", "AIN2", "AIN0", "AIN1","AIN3", "AIN5"]

#Reset pushbutton
RESET = "P8_7"
