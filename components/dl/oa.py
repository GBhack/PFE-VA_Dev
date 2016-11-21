"""
    oa.py
    Decision Level module : Obstacle Avoidance
    Periodically checks the frontal distance and brakes if necesssary
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit
import time

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.ports import DL as DL_PORTS
from robotBasics.constants.ports import ECL as ECL_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER

UPDATE_RATE = 0.1
MINIMAL_DISTANCE = 0.08

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### CLIENTS CONNECTION :

#Creating the Get Frontal Distance module's client
UC_CLIENT = SOCKETS.tcp.Client.Client(ECL_PORTS["usc"], LOGGER)

#We'll send booleans (request)
UC_CLIENT.set_sending_datagram(['BOOL'])
#We'll receive floats (distance in meters)
UC_CLIENT.set_receiving_datagram(['BOOL'])

#Opening the connection
UC_CLIENT.set_up_connection()


#Creating the Velocity/Steering regulator module's client object
VE_CLIENT = SOCKETS.tcp.Client.Client(DL_PORTS["ve"]["oa"], LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(VE_CLIENT.close)

#We'll send floats (distance in meters)
VE_CLIENT.set_sending_datagram(['BOOL'])

#Opening the connection
VE_CLIENT.set_up_connection()

alive = True
print('Running ')
while alive:
    obstacleDetected = False
    UC_CLIENT.send_data([True])
    #print('Request sent to uc, waiting...')
    time.sleep(0.01)
    if UC_CLIENT.receive_data():
        time.sleep(0.01)
        UC_CLIENT.send_data([True])
        if UC_CLIENT.receive_data():
            obstacleDetected = True
            #print('obstacle !')
    VE_CLIENT.send_data([obstacleDetected])
    time.sleep(UPDATE_RATE)
