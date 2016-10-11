"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(1300)

TCP.set_sending_datagram(['BOOL'])
TCP.set_receiving_datagram(['FLOAT'])

TCP.set_up_connexion(30)

while 1:

    TCP.send_data([True])
    print('Init')

    print('Received data :'+ str(TCP.receive_data()[0]))

    time.sleep(2)

atexit.register(TCP.close)
