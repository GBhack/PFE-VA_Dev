"""
    For udp server's methods and classes testing
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import sys
import robotBasics as RB

TEST = sys.argv[1]

def print_message(message):
    """
        Callback method for printing a message
    """
    print(message)


SOCKETS = RB.sockets

UDP = SOCKETS.udp.Server.Server(12345)

UDP.send_to_clients(TEST)

UDP.close()
