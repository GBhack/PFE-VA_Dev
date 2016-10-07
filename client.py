"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB
import atexit

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(12345)

TCP.set_sending_datagram(['BOOL'])
TCP.set_receiving_datagram(['FLOAT'])

TCP.set_up_connexion()

TCP.send_data([True])

print(TCP.receive_data()[0])

atexit.register(TCP.close)
