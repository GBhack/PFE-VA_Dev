"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit

from robotBasics.logger import logger as LOGGER

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(1600,LOGGER)

atexit.register(TCP.close)

TCP.set_sending_datagram(['BOOL'])
TCP.set_receiving_datagram(['BOOL'])

if TCP.set_up_connection(600):

    while 1:

        TCP.send_data([True])
        time.sleep(0.5)
        print(TCP.receive_data())
        time.sleep(2)
