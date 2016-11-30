"""
    Server.py
    Defines the Server Class
    Handles the "master" part of a connection
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import socket
import time
import threading

#Specific imports :
from ..datahandling import Message
from ...constants.misc import SOCKETS as MISC_CONST

class Server(object):
    """
        Server Class
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
            self._connectionTimeOut = MISC_CONST["connectionTimeout"]

        #LISTENING TIMEOUT :
        if "listeningTimeOut" in connectionSettings:
            assert connectionSettings["listeningTimeOut"] > 0,\
                "listening timeout parameter MUST be positive"
            assert isinstance(connectionSettings["listeningTimeOut"], int),\
                "listening timeout parameter MUST be an integer"
            self._listeningTimeOut = connectionSettings["listeningTimeOut"]
        else:
            message += '\nno listening-timeout provided, setting defaut.'
            self._listeningTimeOut = MISC_CONST["listeningTimeOut"]

        #NUMBER OF CLIENTS :
        if "numberOfClients" in connectionSettings:
            assert connectionSettings["numberOfClients"] > 0,\
                "number of clients MUST be positive"
            assert isinstance(connectionSettings["numberOfClients"], int),\
                "number of clients MUST be an integer"
            self._numberOfClients = connectionSettings["numberOfClients"]
        else:
            message += '\nno number of clients provided, setting defaut (1).'
            self._numberOfClients = 1

        #DATAGRAMS :
        self._datagrams = {}
        datagramsSet = 0
        assert "datagrams" in connectionSettings,\
            "Missing \"datagrams\" entry in the connection-settings dictionary"
        if "serverToClient" in connectionSettings["datagrams"]:
            self._datagrams["sending"] = \
                Message.Message(connectionSettings["datagrams"]["serverToClient"])
            self._log.debug('Sending datagram set to : %s for client socket on port %d',\
                self._datagrams["sending"], self._port)
            datagramsSet += 1
        if "clientToServer" in connectionSettings["datagrams"]:
            self._datagrams["receiving"] = \
                Message.Message(connectionSettings["datagrams"]["clientToServer"])
            self._log.debug('Receiving datagram set to : %s for client socket on port %d',\
                self._datagrams["receiving"], self._port)
            datagramsSet += 1
        assert datagramsSet > 0,\
            "At least one datagram should be set for the connection."

        socket.setdefaulttimeout(self._connectionTimeOut)

        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        self._connections = []
        self.connected = False

    def connect(self):
        """
            Connection method
        """
        initTime = time.time()

        timeOut = False

        clientsConnected = 0
        waitingForClients = True
        print('Port : ', self._port)
        self._socket.bind(('', self._port))
        self._socket.listen(1)

        while waitingForClients:
            try:
                newConnection, _ = self._socket.accept()
                newConnection = {
                    "connection": newConnection,
                    "alive": True
                }
                self._connections.append(newConnection)
                clientsConnected += 1
            except socket.timeout:
                timeOut = True

            if time.time() - initTime > self._connectionTimeOut * self._numberOfClients or timeOut:
                waitingForClients = False
                self._log.warning("Server accepting timed out on port %d: %d client(s) connected",\
                    self._port, clientsConnected)
            if clientsConnected >= self._numberOfClients:
                waitingForClients = False
                self._log.info("Maximum number of clients reached (%d) on port %d.",\
                    clientsConnected, self._port)

        if clientsConnected > 0:
            self.connected = True
        else:
            self._log.warning("No client connected on port %d.",\
                self._port)

        socket.setdefaulttimeout(self._listeningTimeOut)

    def listen_to_clients(self, callback, args):
        """
            Data receiving method
        """

        listeningThread = []

        for client in self._connections:
            threadSettings = {
                "connection": client,
                "datagram": self._datagrams["receiving"],
                "callback": callback,
                "args": args,
                "closingMethod": self.close
            }
            
            listeningThread.append(WaitForData(threadSettings))
            listeningThread[-1].start()

        for thread in listeningThread:
            thread.join()

    def send(self, data):
        """
            Data sending method
        """
        if "sending" in self._datagrams:
            if len(self._connections) <= 0:
                self.connected = False
            if self.connected:
                for connection in self._connections:
                    try:
                        connection["connection"].send(self._datagrams["sending"].encode(data))
                    except:
                        connection["alive"] = False
                        self.close()
                        self._log.error("An error occured : could not send data to \
                            port %d", self._port)
            else:
                self._log.warning("Could not send to port %d (the socket must be \
                    connected in order to send data).", self._port)
        else:
            self._log.warning("Could not send to port %d (the clientToServer datagram \
                must be set).", self._port)

    def close(self):
        """
            Connection closing method
        """
        for connection in self._connections:
            if not connection["alive"]:
                connection["connection"].shutdown(socket.SHUT_RDWR)
                connection["connection"].close()
                self._connections.remove(connection)
                self._log.info("Closed client connection on port %d.", self._port)
        if len(self._connections) == 0:
            self.connected = False
    def __str__(self):
        return "SERVER instance"



class WaitForData(threading.Thread):
    """
        WaitForData Class (threading)
    """

    def __init__(self, threadSettings):
        """
            Initialization
        """
        threading.Thread.__init__(self)
        self.threadSettings = threadSettings 

    def run(self):
        """
            Running (when start is called)
        """
        while self.threadSettings["connection"]["alive"]:
            try:
                data = self.threadSettings["connection"]["connection"]\
                    .recv(self.threadSettings["datagram"].size)
                if data:
                    self.threadSettings["callback"](self.threadSettings["datagram"].decode(data),\
                        self.threadSettings["args"])
                else:
                    self.threadSettings["connection"]["alive"] = False
            except ConnectionResetError:
                self.threadSettings["connection"]["alive"] = False
            except socket.timeout:
                self.threadSettings["connection"]["alive"] = False

        self.threadSettings["closingMethod"]()
