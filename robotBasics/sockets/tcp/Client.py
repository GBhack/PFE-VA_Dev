"""
    Client.py
    Defines the TCP Client class.
    We call "client" the entity that connects to a pre-existing server.
    The client is the "slave" part of the connection.
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
        Client class
    """
    def __init__(self, port):
        """
            Initialization
        """
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def set_sending_datagram(self, datagram):
        """
            Sending-Datagram set method
            [Arguments] :
            - datagram : the message pattern for all data sent (see datahandling's readme)
        """
        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        """
            Receiving-Datagram set method
            [Arguments] :
            - datagram : the message pattern for all data received (see datahandling's readme)
        """
        self._receivingDatagram = Message.Message(datagram)
        self._receivingMessageSize = self._receivingDatagram.size

    def set_up_connection(self, timeout=MISC.SOCKETS["timeout"]):
        """
            Connexion set-up method
        """
        print("CLIENT")
        socket.setdefaulttimeout(timeout)
        try:
            self.connection.connect(('127.0.0.1', self.port))
            return True
        except ConnectionRefusedError:
            print("Connection refused. Is the server running with available sockets ?")
            return False

    def send_data(self, data):
        """
            Data sending method
        """
        self.connection.send(self._sendingDatagram.encode(data))

    def receive_data(self):
        """
            Data sending method
        """
        data = self.connection.recv(self._receivingMessageSize)
        if data:
            return self._receivingDatagram.decode(data)
        else:
            return 0

    def close(self):
        self.connection.close()
        print('Closing')
