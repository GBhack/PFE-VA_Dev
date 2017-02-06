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
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import MOT as MOT_CS
from robotBasics.constants.connectionSettings import VSC as VSC_CS
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.logger import robotLogger

###########################################################################
#                           Environment Setup :                           #
###########################################################################

#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot/'
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    CONFIG_FILE = open(path.expanduser('~/.robotConf'), 'r')
    ROBOT_ROOT = CONFIG_FILE.read().strip()
    CONFIG_FILE.close()
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("ECL > vsc", ROBOT_ROOT+'logs/ecl/')

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
    args["velocityConnection"].send([args["currentState"]["velocity"]])

def steering_control_cb(data, args):
    """
        Steering control callback method
        Apply requested steering
    """
    print('REQUEST RECEIVED !!!!')
    #We apply the change to the program's velocity variable
    args["currentState"]["steeringRatio"] = data[0]

    print('Received steering : ', data[0])
    #We apply the changes to the robot :
    apply_modifications(args)

    #We send the velocity actually applied to the client :
    args["steeringConnection"].send([data[0]])

def apply_modifications(args):
    #Wait for the semaphore to be cleared (so we don't apply two modifications at the same time)
    while args["currentState"]["busy"]:
        time.sleep(0.0001)

    args["currentState"]["busy"] = True

    velocity = args["currentState"]["velocity"]
    steering = args["currentState"]["steeringRatio"]

    #We make sure not to go over 100% velocity on each wheel.
    #If so, we have to reduce the mean velocity :
    factor = 0.01
    if velocity*(1+factor*abs(steering)) > 100:
        velocity = 100/(1+abs(steering)*factor)
    elif velocity*(1+factor*abs(steering)) < -100:
        velocity = -100/(1+abs(steering)*factor)
    leftVelocity = round(velocity*(1+factor*steering))
    rightVelocity = round(velocity*(1-factor*steering))

    args["currentState"]["velocity"] = velocity

    #We apply the changes to the robot :
    try:
        args["leftMotorConnection"].send([leftVelocity])
        args["rightMotorConnection"].send([rightVelocity])
    except:
            print('erreur lors de l\'envoi')
    args["currentState"]["busy"] = False


###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the connection object
CLIENT_LEFT = Client(MOT_CS["LEFT"], LOGGER)
CLIENT_RIGHT = Client(MOT_CS["RIGHT"], LOGGER)

#Opening the connection
CLIENT_LEFT.connect()
CLIENT_RIGHT.connect()

#### SERVER CONNECTION :

## Velocity Server :

#Creating the connection object
VELOCITY_SERVER = Server(VSC_CS["velocity"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VELOCITY_SERVER.close)

#Opening the connection
VELOCITY_SERVER.connect()

## Steering Server :

#Creating the connection object
STEERING_SERVER = Server(VSC_CS["steering"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(STEERING_SERVER.close)

#Opening the connection
STEERING_SERVER.connect()

#### CALLBACKS' ARGUMENTS SETUP:

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


###########################################################################
#                               RUNNING :                                 #
###########################################################################

while not VELOCITY_SERVER.connected or not STEERING_SERVER.connected:
    time.sleep(0.05)

#Waiting for requests and redirecting them to the callback methods
VELOCITY_SERVER.listen_to_clients(velocity_control_cb, ARGUMENTS_VELOCITY)
STEERING_SERVER.listen_to_clients(steering_control_cb, ARGUMENTS_STEERING)

VELOCITY_SERVER.join_clients()
STEERING_SERVER.join_clients()

stopped = False
