"""
    gpiodef.py
    BeagleBone's pins association
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

ENGINES = {
    "left": {
        "PWM":          "P9_16",
        "direction":    "P9_12",
        "enable":       "P9_17"
    },
    "right": {
        "PWM":          "P9_14",
        "direction":    "P9_13",
        "enable":       "P9_15"
    }
}

LEDS = {
    "left": "P9_24",
    "right": "P9_23",
    "stop": "P9_25",
    "status": "P9_26"
}

SONAR = {
    "trigger": "P9_28",
    "echo": "P9_29"
}
RESET = "P9_27"


