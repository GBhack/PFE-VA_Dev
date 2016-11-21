"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit
import random

from robotBasics.logger import logger as LOGGER

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(2300, LOGGER)

atexit.register(TCP.close)

TCP.set_sending_datagram([['BITS', [2, 1]]])
TCP.set_receiving_datagram(['BOOL'])

myList = [[0, 0], [0,1], [1,1], [0, 1], [0, 0], [2,1]]
if TCP.set_up_connection(600):

    for item in myList:
        #led = random.randrange(0, 4, 1)
        #state = random.randrange(0, 2, 1)
        TCP.send_data([item])
        print(TCP.receive_data())
        time.sleep(0.5)
