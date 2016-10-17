"""
    constants.py
    TCP/UDP ports constants
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Functional Level module's ports
FL = {
    "pb":   1000,
    "qe":   1100,
    "lf":   1200,
    "us":   1300,
    "led":  1400,
    "mot":  {
        "left":   1500,
        "right":  1510
    }
}

ECL = {
    "gcd":  2000,
    "gfd":  2100,
    "gori": 2200,
    "vsc":  {
        "velocity":     2300,
        "radius":       2310
    },
    "gtls": 2400
}

DL = {
    "KOT":  3000,
    "BCR":  3100,
    "AI":   3200,
    "YR":   3300,
    "OA":   3400,
    "CTL":  3500
}
