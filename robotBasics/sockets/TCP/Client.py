#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import socket
import time


class Client:

	def __init__(self,port,datagram):
		self.port = port

	def setUpConnexion(self,timeout = 5) :

		socket.setdefaulttimeout(timeout)

		self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connexion.connect(('127.0.0.1',self.port))

	def sendData(self, data) :
		self.connexion.send(data.encode())