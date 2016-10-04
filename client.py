#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB

sockets = RB.sockets

TCP = sockets.TCP.Client.Client(12345,0)

TCP.setUpConnexion()

TCP.sendData('Test 123')