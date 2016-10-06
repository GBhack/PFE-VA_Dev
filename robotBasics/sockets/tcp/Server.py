"""
    Server.py
    Server Class
    Handle the "master" part of a connexion
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import socket
import time

from threading import Thread

from ..datahandling import Message

class Server(object):
    """
        Class Server
    """


    def __init__(self, port, datagram, frequency=0.1):
        """
            Initialization
        """
        self._port = port
        self._frequency = frequency
        self._connexions = []
        self._datagram = Message.Message(datagram)

    def set_up_connexion(self, timeout=5, multiClients=False, maxClients=2):
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
                self._connexions.append(newConnexion)
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

    def listen_to_clients(self, callback):
        """
            Listening to clients Method
        """
        threads = []
        for connexion in self._connexions:
            threads.append(WaitForData(connexion, self._datagram, callback, self._frequency))
            threads[-1].start()


class WaitForData(Thread):
    """
        WaitForData Class (threading)
    """

    def __init__(self, connexion, datagram, callback, frequency):
        """
            Initialization
        """
        Thread.__init__(self)
        self.callback = callback
        self.connexion = connexion
        self._frequency = frequency
        self._datagram = datagram
        self._messageSize = datagram.get_size()

    def run(self):
        """
            Running (when start is called)
        """
        while True:
            data = self.connexion.recv(self._messageSize)
            if data:
                self.callback(self._datagram.decode(data))
            time.sleep(self._frequency)
