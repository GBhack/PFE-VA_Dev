"""

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time
import atexit

#Specific imports :
import robotBasics as RB
from robotBasics.logger import logger as LOGGER

CONSTANTS = RB.constants
SOCKETS = RB.sockets

#Creating the TCP instances
CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["left"],LOGGER)
time.sleep(0.001)
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Client.Client(RB.constants.ports.FL["mot"]["right"],LOGGER)
time.sleep(0.001)

#We'll send small signed integers (-100 -> 100% of thrust / steering radius)
CONNECTION_MOTOR_LEFT.set_sending_datagram(['SMALL_INT_SIGNED'])
CONNECTION_MOTOR_RIGHT.set_sending_datagram(['SMALL_INT_SIGNED'])

#We'll receive booleans (status of the operation)
CONNECTION_MOTOR_LEFT.set_receiving_datagram(['BOOL'])
CONNECTION_MOTOR_RIGHT.set_receiving_datagram(['BOOL'])

#Opening the connection
CONNECTION_MOTOR_LEFT.set_up_connection(100)
CONNECTION_MOTOR_RIGHT.set_up_connection(100)

CONNECTION_MOTOR_LEFT.send_data([0])
CONNECTION_MOTOR_RIGHT.send_data([10])
