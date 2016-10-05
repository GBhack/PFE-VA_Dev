"""
    Client.py
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import socket

from ..datahandling import Message


class Client:
    """
        class Client
    """
    def __init__(self, port, datagram):
        """
            Initialization
        """
        self.port = port
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._datagram = Message.Message(datagram)

    def set_up_connexion(self, timeout=5):
        """
            Connexion set-up method
        """
        socket.setdefaulttimeout(timeout)
        self.connexion.connect(('127.0.0.1', self.port))

    def send_data(self, data):
        """
            Data sending method
        """
        self.connexion.send(self._datagram.encode(data))
