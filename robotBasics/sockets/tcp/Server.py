"""
    Server.py
    Server Class
    Handle the "master" part of a connexion
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import socket
import time

import threading

from ..datahandling import Message
from ...constants import misc as MISC

class Server(object):
    """
        Class Server
    """


    def __init__(self, port, frequency=MISC.SOCKETS["frequency"]):
        """
            Initialization
        """
        self._port = port
        self._frequency = frequency
        self._connexions = []
        self._clientsListeningThreads = []

    def set_sending_datagram(self, datagram):
        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        self._receivingDatagram = Message.Message(datagram)

    def set_up_connexion(self, timeout=MISC.SOCKETS["timeout"], multiClients=False, maxClients=2):
        """
            Connexion set-up method
            Arguments :
                - timeout : the amount of time the server waits
                for something to happen before raising an error
                - multiClients
        """
        socket.setdefaulttimeout(timeout)

        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.bind(('', self._port))
        newSocket.listen(1)

        waitForClient = True
        clientsConnected = 0
        socketCreationTime = time.time()

        while waitForClient:
            try:
                newConnexion, _ = newSocket.accept()
                self._connexions.append({"sock": newConnexion, "stopEvent":threading.Event()})
                clientsConnected += 1
                if clientsConnected >= maxClients or not multiClients:
                    print('Maximum amount of clients reached (', clientsConnected, ')')
                    waitForClient = False
                if time.time() - socketCreationTime > timeout:
                    print("Timeout : ", clientsConnected, " clients connected")
                    waitForClient = False
            except socket.timeout:
                print("Timeout : ", clientsConnected, " clients connected")
                waitForClient = False

        if clientsConnected > 0:
            print("Success !")

    def listen_to_clients(self, callback, args):
        """
            Listening to clients Method
        """
        for connexion in self._connexions:
            self._clientsListeningThreads.append(WaitForData(connexion["sock"], self._receivingDatagram, callback, args, self._frequency, connexion["stopEvent"]))
            self._clientsListeningThreads[-1].start()

    def send_to_clients(self, data):
        """
            Send to clients Method
        """
        for connexion in self._connexions:
            connexion["sock"].send(self._sendingDatagram.encode(data))

    def close(self):
        for connexion in self._connexions:
            connexion["stopEvent"].set()
            time.sleep(0.01)
            connexion["sock"].close()
            print('Closing')
        for thread in self._clientsListeningThreads:
            thread.join()

class WaitForData(threading.Thread):
    """
        WaitForData Class (threading)
    """

    def __init__(self, connexion, datagram, callback, args, frequency, stopEvent):
        """
            Initialization
        """
        threading.Thread.__init__(self)
        self.callback = callback
        self.connexion = connexion
        self._frequency = frequency
        self._datagram = datagram
        self._messageSize = datagram.get_size()
        print('Message size : '+str(self._messageSize))
        self._stopEvent = stopEvent
        self._args = args

    def run(self):
        """
            Running (when start is called)
        """
        while not self._stopEvent.is_set():
            data = self.connexion.recv(self._messageSize)
            if data:
                self.callback(self._datagram.decode(data), self._args)
            time.sleep(self._frequency)
