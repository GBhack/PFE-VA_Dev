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

#Specific imports :
from ..datahandling import Message


class Server(object):
    """
        Class Server
    """


    def __init__(self, port):
        """
            Initialization
        """
        self._connexionInfo = ("127.255.255.255", port)

        #Configure the socket tu use UDP
        self._sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #Configure the socket to broadcast packets
        self._sendingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        self._creationTime = time.time()

    def set_sending_datagram(self, datagram):
        """
            Handles the packing process for data to send
        """

        self._sendingDatagram = Message.Message(datagram)

    def get_socket_creation_time(self):
        """
            Getter : retrieve the socket creation time
        """
        return self._creationTime



    def send_to_clients(self, data):
        """
            Send to clients Method
        """
        self._sendingSocket.sendto(self._sendingDatagram.encode(data), self._connexionInfo)


    def close(self):
        """
            Closing socket
        """
        self._sendingSocket.close()
        print('UDP Socket closed')
