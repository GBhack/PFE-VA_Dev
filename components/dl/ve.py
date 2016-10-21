"""
    ve.py
    Decision Level module : Velocity Executor
    Executes the velocity plan while handeling emergency brake
    if requested by the oa module.
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time
import atexit

#Specific imports :
from robotBasics import constants as CONSTANTS
from robotBasics import sockets as SOCKETS

VELOCITY_STATE = {
    "busy": False,
    "oa_brake": False,
    "actualVelocity": 0,
    "desiredVelocity": 0
}

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def oa_handling_cb(data, args):
    if data[0]:
        while  args["velocity_state"]["busy"]:
            time.sleep(0.0001)
        args["velocity_state"]["busy"] = True
        args["velocity_state"]["oa_brake"] = True
        args["velocity_state"]["desiredVelocity"]
        args["velocity_client"].send_data([0])
        _ = args["velocity_client"].receive_data()
        args["velocity_state"]["busy"] = False
    else:
        args["oa_brake"] = False

def velocity_handling_cb(data, args):

    while  args["velocity_state"]["busy"]:
        time.sleep(0.0001)
    args["velocity_state"]["busy"] = True
    args["velocity_state"]["desiredVelocity"] = data[0]
    args["velocity_server"].send_to_clients([True])
    args["velocity_state"]["busy"] = False

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#
VELOCITY_CLIENT = SOCKETS.tcp.Client.Client(CONSTANTS.ports.ECL["vsc"]["velocity"])

#We'll send booleans (request)
VELOCITY_CLIENT.set_sending_datagram(['FLOAT'])
#We'll receive floats (distance in meters)
VELOCITY_CLIENT.set_receiving_datagram(['FLOAT'])

#Opening the connection
VELOCITY_CLIENT.set_up_connection()

#### SERVER CONNECTION :

#Creating the TCP instances
OA_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.DL["ve"]["oa"])
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(OA_SERVER.close)

#We'll receive booleans (status of the operation)
OA_SERVER.set_receiving_datagram(['BOOL'])

#Opening the connection
OA_SERVER.set_up_connection(10)

## Velocity Server :

#Creating the TCP instance
VELOCITY_SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.DL["ve"]["velocity"])
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VELOCITY_SERVER.close)

#We'll receive and send small integers (velocity in percent of nominal velocity)
VELOCITY_SERVER.set_receiving_datagram(['FLOAT'])
VELOCITY_SERVER.set_sending_datagram(['BOOL'])

#Opening the connection
VELOCITY_SERVER.set_up_connection(600)

OA_ARGUMENTS = {
    "velocity_state": VELOCITY_STATE,
    "velocity_client": VELOCITY_CLIENT
}

VELOCITY_ARGUMENTS = {
    "velocity_state": VELOCITY_STATE,
    "velocity_server": VELOCITY_SERVER
}

#Waiting for requests and redirecting them to the callback methods
VELOCITY_SERVER.listen_to_clients(velocity_handling_cb, VELOCITY_ARGUMENTS)
OA_SERVER.listen_to_clients(oa_handling_cb, OA_ARGUMENTS)

alive = True

while alive:
    if VELOCITY_STATE["oa_brake"]:
        desiredVelocity = 0
    else:
        desiredVelocity = VELOCITY_STATE["desiredVelocity"]
    if VELOCITY_STATE["actualVelocity"] != desiredVelocity:
        VELOCITY_CLIENT.send_data([desiredVelocity])
        VELOCITY_STATE["actualVelocity"] = VELOCITY_CLIENT.receive_data()
