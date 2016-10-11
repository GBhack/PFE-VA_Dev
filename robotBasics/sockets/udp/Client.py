"""
    Client.py
    Defines the UDP Client class.
    We call "client" the entity that waits for the data sent by the server.
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import socket
import threading

#Specific imports :
#from ..datahandling import Message


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

    def set_up_connexion(self, callback):
        connexion = WaitForData(callback, self._sendingSocket)
        connexion.start()


    def set_receiving_datagram(self, datagram):
        """
            Decode the data sent
        """
        # self._receivingDatagram = Message.Message(datagram)
        # self._receivingMessageSize = self._receivingDatagram.get_size()

    def receive_data(self):
        """
            Data sending method
        """
        data = self._sendingSocket.recv(7) #self._receivingMessageSize)
        if data:
            return data.decode() #self._receivingDatagram.decode(data)
        else:
            return 0

    def close(self):
        """
            Dispose the socket's binding 
        """
        self._sendingSocket.close()
        print('Closing')

class WaitForData(threading.Thread):
    """
        Thread for data receiving
    """

    def __init__(self, callback, connexion):

        threading.Thread.__init__(self)
        self.callback = callback
        self.connexion = connexion
        
    def run(self):
        """
            Running (when start is called)
        """
        while 1:
            print('Waiting for data')
            data = self.connexion.recv(1024)
            if data:
                self.callback(data.decode())

