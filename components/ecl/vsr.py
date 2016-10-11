"""
    vsr.py
    Execution Control Level module : Velocity/Steering Regulator
    Handles the two motors in order to obtain desired velocity
    and steering radius while allowing emergency braking at any time.
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time

#Specific imports :
import robotBasics as RB

CONSTANTS = RB.constants

SOCKETS = RB.sockets

#Creating the Get Frontal Distance module's client
VELOCITY_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsr"]["velocity"])

#We'll receive small integers (velocity in percent of nominal velocity)
VELOCITY_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])

#Opening the connexion
VELOCITY_SERVER.set_up_connexion()


#Creating the Get Frontal Distance module's client
RADIUS_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsr"]["radius"])

#We'll receive small integers (velocity in percent of nominal velocity)
RADIUS_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])

#Opening the connexion
RADIUS_SERVER.set_up_connexion()


#Creating the Get Frontal Distance module's client
BRAKE_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsr"]["brake"])

#We'll receive small integers (velocity in percent of nominal velocity)
BRAKE_SERVER.set_receiving_datagram(['BOOL'])

#Opening the connexion
BRAKE_SERVER.set_up_connexion(MISC.SOCKETS["timeout"], True, 2)

stopped = False
