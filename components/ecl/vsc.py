"""
    vsc.py
    Execution Control Level module : Velocity/Steering Controler
    Controls the PWM module’s state in order to get desired velocity
    (in % of Vmax) and steering radius (in % of Rmax)
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time
import atexit

#Specific imports :
import robotBasics as RB

CONSTANTS = RB.constants
SOCKETS = RB.sockets

def velocity_control_cb(data, args):
    """
        Velocity control callback method
    """
    deltaVelocity = data[0] - args["currentState"]["velocity"]

    #If we're accelerating :
    if abs(data[0]) > abs(args["currentState"]["velocity"]):
        if abs(args["currentState"]["velocity"]) < 20:
            if deltaVelocity < -2:
                deltaVelocity = -2
            elif deltaVelocity > 2:
                deltaVelocity = 2
        elif abs(args["currentState"]["velocity"]) < 50:
            if deltaVelocity < -5:
                deltaVelocity = -5
            elif deltaVelocity > 5:
                deltaVelocity = 5
        else:
            if deltaVelocity < -10:
                deltaVelocity = -10
            elif deltaVelocity > 10:
                deltaVelocity = 10

    args["currentState"]["velocity"] += deltaVelocity
    print('received')
    apply_modifications(args)
    args["connection"].send_to_clients([args["currentState"]["velocity"]])

def steering_control_cb(data, args):
    """
        Velocity control callback method
    """
    args["currentState"]["steeringRatio"] = data[0]
    apply_modifications(args)
    args["connection"].send_to_clients([data[0]])

def apply_modifications(args):
    leftVelocity = args["currentState"]["velocity"] - args["currentState"]["steeringRatio"] / 2
    rightVelocity = args["currentState"]["velocity"] + args["currentState"]["steeringRatio"] / 2

    leftVelocity = args["currentState"]["velocity"]
    rightVelocity = args["currentState"]["velocity"]
    args["motorLeft"].send_data([leftVelocity])
    args["motorRight"].send_data([rightVelocity])


CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["left"])
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["right"])

#We'll send booleans (status of the operation)
CONNECTION_MOTOR_LEFT.set_sending_datagram(['SMALL_INT_SIGNED'])
CONNECTION_MOTOR_RIGHT.set_sending_datagram(['SMALL_INT_SIGNED'])

#We'll receive small signed integers (-100 -> 100% of thrust)
CONNECTION_MOTOR_LEFT.set_receiving_datagram(['BOOL'])
CONNECTION_MOTOR_RIGHT.set_receiving_datagram(['BOOL'])

CONNECTION_MOTOR_LEFT.set_up_connection()
time.sleep(0.1)
CONNECTION_MOTOR_RIGHT.set_up_connection()

#Creating the Get Frontal Distance module's client
VELOCITY_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsc"]["velocity"])
atexit.register(VELOCITY_SERVER.close)

#We'll receive small integers (velocity in percent of nominal velocity)
VELOCITY_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
VELOCITY_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])
#Opening the connection
VELOCITY_SERVER.set_up_connection(600)


STEERING_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsc"]["radius"])

STEERING_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
STEERING_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])

STEERING_SERVER.set_up_connection(600)

CURRENT_STATE = {
    "velocity": 0,
    "steeringRatio"  : 0,
    "steeringRight": True
}


ARGUMENTS_VELOCITY = {
    "currentState" : CURRENT_STATE,
    "connection": VELOCITY_SERVER,
    "motorLeft": CONNECTION_MOTOR_LEFT,
    "motorRight": CONNECTION_MOTOR_RIGHT
}

ARGUMENTS_STEERING = {
    "currentState" : CURRENT_STATE,
    "connection": VELOCITY_SERVER,
    "motorLeft": CONNECTION_MOTOR_LEFT,
    "motorRight": CONNECTION_MOTOR_RIGHT
}

VELOCITY_SERVER.listen_to_clients(velocity_control_cb, ARGUMENTS_VELOCITY)
STEERING_SERVER.listen_to_clients(steering_control_cb, ARGUMENTS_STEERING)


CONNECTION_MOTOR_LEFT.send_data([75])
time.sleep(0.01)
CONNECTION_MOTOR_RIGHT.send_data([-53])
time.sleep(0.01)
CONNECTION_MOTOR_LEFT.send_data([90])
time.sleep(0.01)
CONNECTION_MOTOR_RIGHT.send_data([-75])


stopped = False
