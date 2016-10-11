"""
    Client.py
    Defines the UDP Client class.
    We call "client" the entity that waits for the data sent by the server.
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

class Client:
    """
        class Client
    """
    def __init__(self, port, frequency=MISC.SOCKETS["frequency"]):
        """
            Initialization
        """

        self._connexionInfo = ("127.255.255.255", port)

        self._frequency = frequency

        self._stopEvent = threading.Event()

        #Configure the socket tu use UDP
        self._sendingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        #Configure the socket to allow other process to use the port (for broadcasting)
        self._sendingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        

    def set_up_connexion(self):
        
        self._sendingSocket.bind(self._connexionInfo)
        

    def listen_to_server(self, callback, args):
        
        connexion = WaitForData(self._sendingSocket, self._receivingDatagram, callback, args, self._frequency, self._stopEvent)     
        connexion.start()

    def set_receiving_datagram(self, datagram):
        """
            Decode the data sent
        """
        self._receivingDatagram = Message.Message(datagram)
        # self._receivingMessageSize = self._receivingDatagram.get_size()

    def close(self):
        """
            Dispose the socket's binding 
        """
        self._stopEvent.set()
        time.sleep(0.001)
        self._sendingSocket.close()
        print('Closing')

class WaitForData(threading.Thread):
    """
        Thread for data receiving
    """

    def __init__(self, connexion, datagram, callback, args, frequency, stopEvent):

        threading.Thread.__init__(self)
        self._connexion = connexion
        self._callback = callback
        self._datagram = datagram
        self._args = args
        self._frequency = frequency
        self._stopEvent = stopEvent

        
        
    def run(self):
        """
            Running (when start is called)
        """
        while not self._stopEvent.is_set():
            data = self._connexion.recv(self._datagram.size)
            if data:
                self._callback(self._datagram.decode(data), self._args)

