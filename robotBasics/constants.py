"""
    constants.py
"""
"""
    Constants and BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

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

LEDS = {
    "left": "GPIO0_15",
    "right": "GPIO0_49",
    "stop": "GPIO0_117",
    "status": "GPIO0_14"
}
