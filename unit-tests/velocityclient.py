"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(3110)

atexit.register(TCP.close)

TCP.set_sending_datagram(['SMALL_INT_SIGNED'])
TCP.set_receiving_datagram(['SMALL_INT_SIGNED'])

if TCP.set_up_connection(600):

    while 1:

        value = int(input("Velocity ?"))
        if value <= 100 and value >= -100:
            try:
                TCP.send_data([int(value)])
            except:
                print('erreur lors de l\'envoi')
            time.sleep(0.05)
            print(TCP.receive_data())
