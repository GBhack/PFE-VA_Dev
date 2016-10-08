"""
    gpiodef.py
    BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Engines-related I/O :
ENGINES = {
    "left": {
        "PWM":          "GPIO0_51",
        "direction":    "GPIO0_60",
        "enable":       "GPIO0_05"
    },
    "right": {
        "PWM":          "GPIO0_50",
        "direction":    "GPIO0_31",
        "enable":       "GPIO0_48"
    }
}

#LEDs-related I/O :
LEDS = {
    "left": "GPIO0_15",
    "right": "GPIO0_49",
    "stop": "GPIO0_117",
    "status": "GPIO0_14"
}

#Sonar-related I/O :
SONAR = {
    "trigger": "GPIO0_123",
    "echo": "GPIO0_121"
}

#Reset pushbutton
RESET = "GPIO0_115"
