#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import socket
import time
from threading import Thread

class Server:


	def __init__(self,port,datagram,frequency = 0.1):
		self.port = port
		self.frequency = frequency
		self.connexions = []

	def setUpConnexion(self,timeout = 5, multiClients = False, maxClients = 2) :

		socket.setdefaulttimeout(timeout)

		newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		newSocket.bind(('', self.port))
		newSocket.listen(1)

		waitForClient = True
		clientsConnected = 0
		socketCreationTime = time.time()

		while waitForClient :
			try:
				newConnexion, addr = newSocket.accept()
				self.connexions.append(newConnexion)
				clientsConnected+=1
				if (clientsConnected >= maxClients) or (multiClients == False) :
					print('Maximum amount of clients reached (',clientsConnected,')')
					waitForClient = False
				if (time.time()-socketCreationTime > timeout):
					print("Timeout : ",clientsConnected," clients connected")
					waitForClient = False
			except socket.timeout :
				print("Timeout : ",clientsConnected," clients connected")
				waitForClient = False

		if(clientsConnected > 0) :
			print("Success !")

	def listenToClients(self,callback) :
		threads = []
		for connexion in self.connexions :
			threads.append(WaitForData(connexion,callback,self.frequency))
			threads[-1].start()

class WaitForData(Thread):

	def __init__(self,connexion,callback,frequency) :
		Thread.__init__(self)
		self.callback = callback
		self.connexion = connexion
		self.frequency = frequency

	def run(self) :

		while True:
			 data = self.connexion.recv(1024)
			 if data :
			 	self.callback(data.decode())
			 time.sleep(self.frequency)
