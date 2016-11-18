"""
    qeclient.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import atexit

import robotBasics as RB
from robotBasics import constants as CONSTANTS


from robotBasics.logger import logger as LOGGER

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(CONSTANTS.ports.FL["os"], LOGGER)

atexit.register(TCP.close)

TCP.set_sending_datagram(['BOOL'])
TCP.set_receiving_datagram([['BITS', [1,1,1,1,1,1,1]]])

if TCP.set_up_connection(600):

    while 1:

        TCP.send_data([True])
        time.sleep(0.5)
        print(TCP.receive_data())
        time.sleep(2)
