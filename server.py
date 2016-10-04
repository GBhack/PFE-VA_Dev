#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB

def printMessage(message):
	print('Message : ',message)

sockets = RB.sockets

TCP = sockets.TCP.Server.Server(12345,0)

TCP.setUpConnexion(5,True,2)


TCP.listenToClients(printMessage)