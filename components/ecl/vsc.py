"""
    vsc.py
    Execution Control Level module : Velocity/Steering Controler
    Controls the PWM module’s state in order to get desired velocity
    (in % of Vmax) and steering radius (in % of Rmax)
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
import time

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import MOT as MOT_CS
from robotBasics.constants.ports import ECL as SERVER_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import robotLogger

LOGGER = robotLogger("ECL > vsc")

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def velocity_control_cb(data, args):
    """
        Velocity control callback method
        Apply requested velocity while making sure not to perform strong accelerations.
    """
    print('Received : '+str(data[0]))
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
    print('Applying modif :')
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
    steering = args["currentState"]["steeringRatio"]

    #We make sure not to go over 100% velocity on each wheel.
    #If so, we have to reduce the mean velocity :
    if velocity*(1+0.005*abs(steering)) > 100:
        velocity = 100/(1+abs(steering)*0.005)
    elif velocity*(1+0.005*abs(steering)) < -100:
        velocity = -100/(1+abs(steering)*0.005)
    leftVelocity = round(velocity*(1+0.005*steering))
    rightVelocity = round(velocity*(1-0.005*steering))

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

#Creating the connection object
CLIENT_LEFT = SOCKETS.tcp.Client.Client(MOT_CS, LOGGER)
CLIENT_RIGHT = SOCKETS.tcp.Client.Client(MOT_CS, LOGGER)

#Opening the connection
CLIENT_LEFT.connect()
CLIENT_RIGHT.connect()

#### SERVER CONNECTION :

## Velocity Server :

#Creating the connection object
VELOCITY_SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["vsc"]["velocity"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VELOCITY_SERVER.close)

#We'll receive and send small integers (% of max velocity)
VELOCITY_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
VELOCITY_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])

#Opening the connection
VELOCITY_SERVER.set_up_connection()

## Steering Server :

#Creating the connection object
STEERING_SERVER = SOCKETS.tcp.Server.Server(SERVER_PORTS["vsc"]["radius"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(STEERING_SERVER.close)

#We'll receive and send small integers (% of max steering)
STEERING_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
STEERING_SERVER.set_sending_datagram(['SMALL_INT_SIGNED'])

#Opening the connection
STEERING_SERVER.set_up_connection()

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
    "leftMotorConnection": CLIENT_LEFT,
    "rightMotorConnection": CLIENT_RIGHT
}

#Argument to be passed to the steering callback method
ARGUMENTS_STEERING = {
    "currentState" : CURRENT_STATE,
    "steeringConnection": STEERING_SERVER,
    "leftMotorConnection": CLIENT_LEFT,
    "rightMotorConnection": CLIENT_RIGHT
}

#Waiting for requests and redirecting them to the callback methods
VELOCITY_SERVER.listen_to_clients(velocity_control_cb, ARGUMENTS_VELOCITY)
STEERING_SERVER.listen_to_clients(steering_control_cb, ARGUMENTS_STEERING)


stopped = False
