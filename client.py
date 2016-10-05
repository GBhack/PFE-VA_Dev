"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB

SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Client.Client(12345, ['SMALL_INT', ['BITS', [2, 1, 3]], 'SMALL_INT', 'LARGE_INT_SIGNED', 'FLOAT', 'BOOL', 'BYTE'])

TCP.set_up_connexion()

TCP.send_data([0, [3, 1, 5], 54, -23785, 17.33451, True, int(17).to_bytes(1, byteorder='big')])
