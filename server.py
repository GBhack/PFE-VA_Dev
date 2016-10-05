"""
    For tcp server's methods and classes testing
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB

def print_message(message):
    """
        Callback method for printing a message
    """
    print(message)


SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Server.Server(12345, ['SMALL_INT', ['BITS', [2, 1, 3]], 'SMALL_INT', 'LARGE_INT_SIGNED', 'FLOAT', 'BOOL', 'BYTE'])

TCP.set_up_connexion(5, True, 2)


TCP.listen_to_clients(print_message)
