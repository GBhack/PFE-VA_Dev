"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import atexit
import robotBasics as RB


def callback_cb(data):
    """
        tata
    """
    print(data)


SOCKETS = RB.sockets
print(1)
UDP = SOCKETS.udp.Client.Client(1051)
print(2)
UDP.set_up_connexion(callback_cb)

print(3)