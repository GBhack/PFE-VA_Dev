"""
    oa.py
    Decision Level module : Obstacle Avoidance
    Periodically checks the frontal distance and brakes if necesssary
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time

#Specific imports :
import robotBasics as RB

CONSTANTS = RB.constants

UPDATE_RATE = 0.2
MINIMAL_DISTANCE = 0.05

SOCKETS = RB.sockets

#Creating the Get Frontal Distance module's client
GFD_CLIENT = SOCKETS.tcp.Client.Client(CONSTANTS.ports.ECL["gfd"])

#We'll send booleans (request)
GFD_CLIENT.set_sending_datagram(['BOOL'])
#We'll receive floats (distance in meters)
GFD_CLIENT.set_receiving_datagram(['FLOAT'])

#Opening the connexion
GFD_CLIENT.set_up_connexion()


#Creating the Velocity/Steering regulator module's client object
VSR_CLIENT = SOCKETS.tcp.Client.Client(CONSTANTS.ports.ECL["vsr"]["brake"])

#We'll send floats (distance in meters)
VSR_CLIENT.set_sending_datagram(['BOOL'])

#Opening the connexion
VSR_CLIENT.set_up_connexion()

stopped = False

while True:
    GFD_CLIENT.send_data([True])
    distance = GFD_CLIENT.receive_data()[0]
    if distance <= MINIMAL_DISTANCE:
        VSR_CLIENT.send_data(True)
        stopped = True
    elif stopped:
        VSR_CLIENT.send_data(False)
        stopped = False
    time.sleep(UPDATE_RATE
