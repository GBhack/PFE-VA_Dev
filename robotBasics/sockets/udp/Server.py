"""
    Server.py
    Defines the Server Class
    Handle the "master" part of a connexion
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import socket
import time
import threading

#Specific imports :
from ..datahandling import Message
from ...constants import misc as MISC


class Server(object):
    """
        Class Server
    """


    def __init__(self, port):
        """
            Initialization
        """
        self._port = port
        self._newSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def set_sending_datagram(self, datagram):
        """
            Handles the packing process for data to send
        """
        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        """
            Handles the unpacking process for data to send
        """
        self._receivingDatagram = Message.Message(datagram)

    def set_up_connexion(self, timeout=MISC.SOCKETS["timeout"]):
        """
            Connexion set-up method
            Arguments :
                - timeout : the amount of time the server waits
                for something to happen before raising an error
                - multiClients
        """
        socket.setdefaulttimeout(timeout)
        socketCreationTime = time.time()


    def send_to_clients(self, data):
        """
            Send to clients Method
        """
        self._newSocket.sendto(self._sendingDatagram.encode(data), ('127.0.0.1', self._port))

    def close(self):
        """
            Closing socket
        """
        self._newSocket.close()
        print('UDP Socket closed')
