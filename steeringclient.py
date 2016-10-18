"""
    steeringclient.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(2310)

atexit.register(TCP.close)

TCP.set_sending_datagram(['SMALL_INT_SIGNED'])
TCP.set_receiving_datagram(['SMALL_INT_SIGNED'])

if TCP.set_up_connection(600):

    while 1:

        value = input("Steering ?")
        TCP.send_data([int(value)])
        time.sleep(0.1)
        print(TCP.receive_data())
