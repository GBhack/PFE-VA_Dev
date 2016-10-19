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

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def velocity_control_cb(data, args):
    """
        Velocity control callback method
        Apply requested velocity while making sure not to perform strong accelerations.
    """
    deltaVelocity = data[0] - args["currentState"]["velocity"]

    #If we're accelerating, we make sure to do so increasingly (if we're braking, we don't care) :
    if abs(data[0]) > abs(args["currentState"]["velocity"]):
        #If we're still under 30% of Vmax, we only allow 5% increments
        if abs(args["currentState"]["velocity"]) < 30:
            if deltaVelocity < -5:
                deltaVelocity = -5
            elif deltaVelocity > 5:
                deltaVelocity = 5
        #Else, wee allow 10% increments
        else:
            if deltaVelocity < -10:
                deltaVelocity = -10
            elif deltaVelocity > 10:
                deltaVelocity = 10

    #We apply the change to the program's velocity variable
    args["currentState"]["velocity"] += deltaVelocity
    #We apply the changes to the robot :
    apply_modifications(args)


    #We send the velocity actually applied to the client :
    args["velocityConnection"].send_to_clients([args["currentState"]["velocity"]])

def steering_control_cb(data, args):
    """
        Steering control callback method
        Apply requested steering
    """
    #We apply the change to the program's velocity variable
    args["currentState"]["steeringRatio"] = data[0]
    #We apply the changes to the robot :
    apply_modifications(args)

    #We send the velocity actually applied to the client :
    args["steeringConnection"].send_to_clients([data[0]])

def apply_modifications(args):
    #Wait for the semaphore to be cleared (so we don't apply two modifications at the same time)
    while args["currentState"]["busy"]:
        time.sleep(0.0001)

    args["currentState"]["busy"] = True

    velocity = args["currentState"]["velocity"]
    steering = args["currentState"]["steering"]

    #We make sure not to go over 100% velocity on each wheel.
    #If so, we have to reduce the mean velocity :
    if velocity*(1+0.005*abs(steering)) > 100:
        velocity = 100/(1+abs(steering)*0.005)
    elif velocity*(1+0.005*abs(steering)) < -100:
        velocity = -100/(1+abs(steering)*0.005)
    leftVelocity = velocity*(1+0.005*steering)
    rightVelocity = velocity*(1-0.005*steering)

    args["currentState"]["velocity"] = velocity

    #We apply the changes to the robot :
    try:
        args["leftMotorConnection"].send_data([leftVelocity])
        args["rightMotorConnection"].send_data([rightVelocity])
    except:
            print('erreur lors de l\'envoi')
    args["currentState"]["busy"] = False


###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the TCP instances
CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["left"])
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["right"])

#We'll send small signed integers (-100 -> 100% of thrust / steering radius)
CONNECTION_MOTOR_LEFT.set_sending_datagram(['SMALL_INT_SIGNED'])
CONNECTION_MOTOR_RIGHT.set_sending_datagram(['SMALL_INT_SIGNED'])

#We'll receive booleans (status of the operation)
CONNECTION_MOTOR_LEFT.set_receiving_datagram(['BOOL'])
CONNECTION_MOTOR_RIGHT.set_receiving_datagram(['BOOL'])

#Opening the connection
CONNECTION_MOTOR_LEFT.set_up_connection()
CONNECTION_MOTOR_RIGHT.set_up_connection()

#### SERVER CONNECTION :

## Velocity Server :

#Creating the TCP instance
VELOCITY_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsc"]["velocity"])
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VELOCITY_SERVER.close)

#We'll receive and send small integers (velocity in percent of nominal velocity)
VELOCITY_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
VELOCITY_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])

#Opening the connection
VELOCITY_SERVER.set_up_connection(600)

## Steering Server :

#Creating the TCP instance
STEERING_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["vsc"]["radius"])
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(STEERING_SERVER.close)

#We'll receive and send small integers (% of max steering)
STEERING_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
STEERING_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])

#Opening the connection
STEERING_SERVER.set_up_connection(600)

## Arguments :

#Shared robot's state :
CURRENT_STATE = {
    "busy":     False,
    "velocity": 0,
    "steeringRatio"  : 0
}

#Argument to be passed to the velocity callback method
ARGUMENTS_VELOCITY = {
    "currentState" : CURRENT_STATE,                 #To "Mix" the 
    "velocityConnection": VELOCITY_SERVER,          #To respond to the request
    "leftMotorConnection": CONNECTION_MOTOR_LEFT,
    "rightMotorConnection": CONNECTION_MOTOR_RIGHT
}

#Argument to be passed to the steering callback method
ARGUMENTS_STEERING = {
    "currentState" : CURRENT_STATE,
    "steeringConnection": STEERING_SERVER,
    "leftMotorConnection": CONNECTION_MOTOR_LEFT,
    "rightMotorConnection": CONNECTION_MOTOR_RIGHT
}

#Waiting for requests and redirecting them to the callback methods
VELOCITY_SERVER.listen_to_clients(velocity_control_cb, ARGUMENTS_VELOCITY)
STEERING_SERVER.listen_to_clients(steering_control_cb, ARGUMENTS_STEERING)


stopped = False
