"""
    For tcp server's methods and classes testing
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB
import time
import atexit

test = [1]

def print_message(message, arg):
    """
        Callback method for printing a message
    """
    print(message)
    arg[0] = message[0]+1


SOCKETS = RB.sockets

TCP = SOCKETS.tcp.Server.Server(1300)

atexit.register(TCP.close)

TCP.set_sending_datagram(['FLOAT'])
TCP.set_receiving_datagram(['BOOL'])

TCP.set_up_connexion(20, True, 2)

while TCP.alive:
    TCP.listen_to_clients(print_message, test)
    TCP.send_to_clients([0.123451])
    time.sleep(1)

TCP.close()


