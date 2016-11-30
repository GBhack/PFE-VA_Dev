"""
    steeringclient.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit
from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.constants.connectionSettings import VSC as VSC_CS
from robotBasics.logger import robotLogger
SOCKETS = RB.sockets

LOGGER = robotLogger("unit-test > steeringclient", '')

TCP = Client(VSC_CS["steering"], LOGGER)

atexit.register(TCP.close)

if TCP.connect():
    while 1:

        value = int(input("Steering ?"))
        if value <= 100 and value >= -100:
            try:
                TCP.send([int(value)])
            except:
                print('erreur lors de l\'envoi')
            time.sleep(0.1)
            print(TCP.receive())
