"""
    Client.py
    Defines the Client Class
    Handles the "slave" part of a connection
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import socket
import time

#Specific imports :
from ..datahandling import Message

class Client(object):
    """
        Client Class
    """

    def __init__(self, connectionSettings, log):
        """
            Initialization
        """

        message = ''

        self._log = log

        #################################################
        #               Settings reading :              #
        #################################################
        
        #PORT :
        assert "port" in connectionSettings,\
            "Missing \"port\" entry in the connection-settings dictionary"
        assert connectionSettings["port"] > 49152 and connectionSettings["port"] < 65535,\
            "Chosen port is out of range, please chose a port number between 49152 and 65535"
        assert isinstance(connectionSettings["port"], int),\
            "the port number MUST be an integer"
        self._port = connectionSettings["port"]

        #CONNECTION TIMEOUT :
        if "connectionTimeout" in connectionSettings:
            assert connectionSettings["connectionTimeout"] > 0,\
                "connection timeout parameter MUST be positive"
            assert isinstance(connectionSettings["connectionTimeout"], int),\
                "connection timeout parameter MUST be an integer"
            self._connectionTimeOut = connectionSettings["connectionTimeout"]
        else:
            message += '\nno connection-timeout provided, setting defaut.'
            self._connectionTimeOut = 2 #####################################REMPLACER PAR MISC CONSTANTE

        #LISTENING TIMEOUT :
        if "listeningTimeOut" in connectionSettings:
            assert connectionSettings["listeningTimeOut"] > 0,\
                "listening timeout parameter MUST be positive"
            assert isinstance(connectionSettings["listeningTimeOut"], int),\
                "listening timeout parameter MUST be an integer"
            self._listeningTimeOut = connectionSettings["listeningTimeOut"]
        else:
            message += '\nno listening-timeout provided, setting defaut.'
            self._listeningTimeOut = 5 #####################################REMPLACER PAR MISC CONSTANTE

        #DATAGRAMS :
        self._datagrams = {}
        self._requestCompatibility = False
        datagramsSet = 0
        assert "datagrams" in connectionSettings,\
            "Missing \"datagrams\" entry in the connection-settings dictionary"
        if "serverToClient" in connectionSettings["datagrams"]:
            self._datagrams["receiving"] = \
                Message.Message(connectionSettings["datagrams"]["serverToClient"])
            self._log.debug('Receiving datagram set to : %s for client socket on port %d',\
                self._datagrams["receiving"], self._port)
            datagramsSet += 1
        if "clientToServer" in connectionSettings["datagrams"]:
            self._datagrams["sending"] = \
                Message.Message(connectionSettings["datagrams"]["clientToServer"])
            self._log.debug('Sending datagram set to : %s for client socket on port %d',\
                self._datagrams["sending"], self._port)
            if connectionSettings["datagrams"]["clientToServer"] == ["BOOL"]:
                self._requestCompatibility = True
                self._log.debug("Sending datagram for client socket on port %d is compatible \
                    with request method usage.", self._port)
            datagramsSet += 1
        assert datagramsSet > 0,\
            "At least one datagram should be set for the connection."

        socket.setdefaulttimeout(self._connectionTimeOut)

        self._connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.connected = False

    def connect(self):

        tryingToConnect = True
        initTime = time.time()

        while tryingToConnect:
            try:
                self._connection.connect(('127.0.0.1', self._port))
                self.connected = True
            except ConnectionRefusedError:
                time.sleep(0.01)
            if self.connected or time.time()-initTime > self._connectionTimeOut:
                tryingToConnect = False
        if self.connected:
            self._log.debug("Connection successful on port %d.", self._port)
            return True
        else:
            self._log.error("Connection refused on port %d. Is the server running \
                with available sockets ?", self._port)
            return False

        socket.setdefaulttimeout(self._listeningTimeOut)

    def receive(self):
        """
            Data receiving method
        """
        if self.connected:
            try:
                data = self._connection.recv(self._datagrams["receiving"].size)
                if not data:
                    self.connected = False
                else:
                    try:
                        return self._datagrams["receiving"].decode(data)
                    except:
                        self._log.error("An error occured : could not decode data \"%s\"  from \
                            port %d. Is the data compliant with the datagram?", data, self._port)
                        return 0
            except:
                self._log.error("An error occured : could not receive data from port %d \
                    in less than %f seconds", self._port, self._listeningTimeOut)
                return 0
        else:
            self._log.warning("Could not receive from port %d (the socket must be connected \
                in order to receive data).", self._port)
            return 0

    def send(self, data):
        """
            Data sending method
        """
        if "sending" in self._datagrams:
            if self.connected:
                try:
                    self._connection.send(self._datagrams["sending"].encode(data))
                    return True
                except (ConnectionResetError, BrokenPipeError):
                    self._log.error("An error occured : could not send data to \
                        port %d", self._port)
                    self.connected = False
                    return False
            else:
                self._log.warning("Could not send to port %d (the socket must be \
                    connected in order to send data).", self._port)
                return False
        else:
            self._log.warning("Could not send to port %d (the clientToServer datagram \
                must be set).", self._port)
            return False

    def request(self):
        """
            Request Method
        """
        if self._requestCompatibility:
            if self.connected:
                self.send([True])
                return self.receive()
            else:
                self._log.warning("Could not request on port %d (the socket must be \
                    connected in order to send data).", self._port)
                return False
        else:
            self._log.warning("Could not send a request to port %d (no clientToServer \
                compatible datagram found).", self._port)

    def close(self):
        self._connection.close()
        self._log.debug("Closed client connection on port %d.", self._port)

    def __str__(self):
        return "CLIENT instance"
