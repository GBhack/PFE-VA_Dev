"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB


def callback_cb(data):
    """
        tata
    """
    print(data)


SOCKETS = RB.sockets
UDP = SOCKETS.udp.Client.Client(12345)
UDP.set_up_connexion(callback_cb)
