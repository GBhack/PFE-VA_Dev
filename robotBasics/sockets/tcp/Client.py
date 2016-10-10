"""
    Client.py
    Defines the TCP Client class.
    We call "client" the entity that connects to a pre-existing server.
    The client is the "slave" part of the connexion.
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import socket

#Specific imports :
from ..datahandling import Message
from ...constants import misc as MISC


class Client:
    """
        class Client
    """
    def __init__(self, port):
        """
            Initialization
        """
        self.port = port
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_sending_datagram(self, datagram):
        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        self._receivingDatagram = Message.Message(datagram)
        self._receivingMessageSize = self._receivingDatagram.get_size()

    def set_up_connexion(self, timeout=MISC.SOCKETS["timeout"]):
        """
            Connexion set-up method
        """
        socket.setdefaulttimeout(timeout)
        self.connexion.connect(('127.0.0.1', self.port))

    def send_data(self, data):
        """
            Data sending method
        """
        self.connexion.send(self._sendingDatagram.encode(data))

    def receive_data(self):
        """
            Data sending method
        """
        data = self.connexion.recv(self._receivingMessageSize)
        if data:
            return self._receivingDatagram.decode(data)
        else:
            return 0

    def close(self):
        self.connexion.close()
        print('Closing')
