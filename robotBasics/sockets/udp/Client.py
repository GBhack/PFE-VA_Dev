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


class Client:
    """
        class Client
    """
    def __init__(self, port):
        """
            Initialization
        """
        self._port = port

        #Broadcasting address
        self._broadcastAddr = "127.255.255.255"

        self._connexionInfo = (self._broadcastAddr, self._port)

        #Configure the socket tu use UDP
        self._sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #Configure the socket to allow other process to use the port (for broadcasting)
        self._sendingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._sendingSocket.bind(self._connexionInfo)
    def set_sending_datagram(self, datagram):
        """
            Encode the data for the sending process
        """

        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        """
            Decode the data sent
        """
        self._receivingDatagram = Message.Message(datagram)
        self._receivingMessageSize = self._receivingDatagram.get_size()

    # def set_up_connexion(self, timeout=MISC.SOCKETS["timeout"]):
    #     """
    #         Connexion set-up method
    #     """
    #     socket.setdefaulttimeout(timeout)
    #     self.connexion.connect(('127.0.0.1', self.port))

    # def send_data(self, data):
    #     """
    #         Data sending method
    #     """
    #     self.connexion.send(self._sendingDatagram.encode(data))

    def receive_data(self):
        """
            Data sending method
        """
        data = self._sendingSocket.recv(self._receivingMessageSize)
        if data:
            return self._receivingDatagram.decode(data)
        else:
            return 0

    def close(self):
        """
            Dispose the socket's binding 
        """
        self._sendingSocket.close()
        print('Closing')

"""
>>> import socket
>>> UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> addr=('',3333)
>>> UDPSock.bind(addr)
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
OSError: [Errno 98] Address already in use
>>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> >>> s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  File "<stdin>", line 1
    >>> s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
     ^
SyntaxError: invalid syntax
>>> s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
>>> s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
>>> s.bind(('127.255.255.255',3333))
>>> s.recvfrom(1024)
(b'coucou', ('127.0.0.1', 46679))
>>> s.recvfrom(1024)
(b'coucou', ('127.0.0.1', 46679))
>>> s.recvfrom(1024)
(b'coucou', ('127.0.0.1', 46679))
>>> 

"""