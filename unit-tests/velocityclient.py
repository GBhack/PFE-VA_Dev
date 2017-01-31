"""
    client.py
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import time
import robotBasics as RB
import atexit
from robotBasics.logger import robotLogger
#from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.constants.connectionSettings import VE as VE_CS
#from robotBasics.constants.connectionSettings import VSC as VSC_CS

LOGGER = robotLogger("unit-test > velocityclient", '')

TCP = Client(VE_CS["velocity"], LOGGER)

atexit.register(TCP.close)

if TCP.connect():

    while 1:

        value = int(input("Velocity ?"))
        if value <= 100 and value >= -100:
            try:
                TCP.send([int(value)])
            except:
                print('erreur lors de l\'envoi')
            time.sleep(0.05)
            print(TCP.receive())
