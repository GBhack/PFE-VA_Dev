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
import time

#Specific imports :
from ..datahandling import Message
from ...constants import misc as MISC


class Client:
    """
        Client class
    """
    def __init__(self, port, log):
        """
            Initialization
        """
        self.port = port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._log = log
        self.connected = False

        log.debug("test")

    def set_sending_datagram(self, datagram):
        """
            Sending-Datagram set method
            [Arguments] :
            - datagram : the message pattern for all data sent (see datahandling's readme)
        """
        self._sendingDatagram = Message.Message(datagram)

        self._log.debug('Sending datagram set to : %s for client socket on port %d', datagram, self.port)

    def set_receiving_datagram(self, datagram):
        """
            Receiving-Datagram set method
            [Arguments] :
            - datagram : the message pattern for all data received (see datahandling's readme)
        """
        self._receivingDatagram = Message.Message(datagram)
        self._receivingMessageSize = self._receivingDatagram.size

        self._log.debug('Receiving datagram set to : %s for client socket on port %d', datagram, self.port)

    def set_up_connection(self, connectionTimeout=MISC.SOCKETS["connectionTimeout"], listeningTimeout=MISC.SOCKETS["listeningTimeout"]):
        """
            Connexion set-up method
        """
        self.listeningTimeout = listeningTimeout

        socket.setdefaulttimeout(listeningTimeout)  #Setting the listening timeout for the connection
        tryingToConnect = True
        connected = False
        initTime = time.time()

        while tryingToConnect:

            try:
                self.connection.connect(('127.0.0.1', self.port))
                connected = True
            except:
                time.sleep(0.01)
            if connected or time.time()-initTime > connectionTimeout:
                tryingToConnect = False
        if connected:
            self.connected = True
            self._log.debug("Connection successful on port %d.", self.port)
            return True
        else:
            self._log.error("Connection refused on port %d. Is the server running with available sockets ?", self.port)
            return False

    def send_data(self, data):
        """
            Data sending method
        """
        if self.connected:
            try:
                self.connection.send(self._sendingDatagram.encode(data))
            except:
                self._log.error("An error occured : could not send data to port %d", self.port)
        else:
            self._log.warning("Could not send to port %d (the socket must be connected in order to send data).", self.port)

    def receive_data(self):
        """
            Data sending method
        """
        if self.connected:
            try:
                data = self.connection.recv(self._receivingMessageSize)
                try:
                    return self._receivingDatagram.decode(data)
                except:
                    self._log.error("An error occured : could not decode data \"%s\" from port %d. Is the data compliant with the datagram?", data, self.port)
                    return 0
            except:
                self._log.error("An error occured : could not receive data from port %d in less than %f seconds", self.port, self.listeningTimeout)
                return 0
        else:
            self._log.warning("Could not send to port %d (the socket must be connected in order to send data).", self.port)
            return 0

    def close(self):
        self.connection.close()
        print('Closing')
