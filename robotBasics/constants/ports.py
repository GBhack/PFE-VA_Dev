"""
    constants.py
    TCP/UDP ports constants
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Functional Level module's ports
FL = {                  # FUNCTIONNAL LEVEL
    "qe":   1000,           # Quadratic Encoder
    "os":   1100,           # Optical Sensors
    "mot":   {              # Motors
        "left":   1200,
        "right":  1210
    },
    "leds":   1300,         # LEDs
    "pb":  1400,            # PushButton
    "ip": 1500,             # Image Processing
    "us": 1600              # Ultrasonic Sensor
}

ECL = {                 # EXECUTION CONTROL LEVEL
    "gsc":  2000,           # General Sensors Controller (QE and OS)
    "vsc":  {               # Velocity/Speed Controller
        "velocity": 2100,
        "radius":   2110
    },
    "lc": 2200,             # LED Controller
    "mc": 2300,             # Mode Controller (Play/Pause/Reset)
    "ipc": 2400,            # Image Processing Controller
    "uc": 2500              # Ultrasonic Controller
}

DL = {                  # DECISION LEVEL
    "pe":  3000,            # Path Executor
    "ve":  {                # Velocity Executor
        "oa": 3100,         # Obstacle Avoidance
        "velocity": 3110,   
        "radius":   3120
    },          
    "pf":   3300,           # Path Following
    "vp":   3400,           # Velocity Planning
    "pp":   3500            # Path Planning
}
