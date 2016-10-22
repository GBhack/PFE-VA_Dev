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
import logging

#Specific imports :
from robotBasics import constants as CONSTANTS
from robotBasics import sockets as SOCKETS



####LOGGER :
formatter = logging.Formatter("%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s")

handler = logging.FileHandler("ve.log", mode="a", encoding="utf-8")

handler.setFormatter(formatter)

handler.setLevel(logging.DEBUG)

logger = logging.getLogger("ve.py")
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


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
        args["velocity_client"].send_data([0])
        _ = args["velocity_client"].receive_data()
        args["velocity_state"]["busy"] = False
    else:
        args["velocity_state"]["oa_brake"] = False

def velocity_handling_cb(data, args):

    while  args["velocity_state"]["busy"]:
        time.sleep(0.001)
    args["velocity_state"]["busy"] = True
    args["velocity_state"]["desiredVelocity"] = int(data[0])
    args["velocity_server"].send_to_clients([True])
    args["velocity_state"]["busy"] = False

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#
VELOCITY_CLIENT = SOCKETS.tcp.Client.Client(CONSTANTS.ports.ECL["vsc"]["velocity"])

#We'll send booleans (request)
VELOCITY_CLIENT.set_sending_datagram(['SMALL_INT_SIGNED'])
#We'll receive floats (distance in meters)
VELOCITY_CLIENT.set_receiving_datagram(['SMALL_INT_SIGNED'])

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
VELOCITY_SERVER.set_receiving_datagram(['SMALL_INT_SIGNED'])
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

print('Running')

while alive:
    if VELOCITY_STATE["oa_brake"]:
        print("Brake")
        desiredVelocity = 0
    else:
        desiredVelocity = int(VELOCITY_STATE["desiredVelocity"])
    if VELOCITY_STATE["actualVelocity"] != desiredVelocity:
        VELOCITY_CLIENT.send_data([desiredVelocity])
        VELOCITY_STATE["actualVelocity"] = VELOCITY_CLIENT.receive_data()
    print('Required velocity : ' + str(desiredVelocity))
    print('Actual velocity : ' + str(VELOCITY_STATE["actualVelocity"]))
    #logger.debug('Required velocity : ' + str(desiredVelocity))
    #logger.debug('Actual velocity : ' + str(VELOCITY_STATE["actualVelocity"]))
    time.sleep(0.25)
