"""
    constants.py
    TCP/UDP ports constants
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Functional Level module's ports
FL = {
    "qe":   1000,
    "os":   1100,
    "mot":   {
        "left":   1200,
        "right":  1210
    },
    "leds":   1300,
    "pb":  1400,
    "ip": 1500,
    "us": 1600
}

ECL = {
    "gsc":  2000,
    "vsc":  {
        "velocity":     2100,
        "radius":       2110
    },
    "lc": 2200,
    "mc": 2300,
    "ipc": 2400,
    "uc": 2500
}

DL = {
    "pe":  3000,
    "ve":  3100,
    "oa":   3200,
    "pf":   3300,
    "vp":   3400,
    "pp":  3500
}
