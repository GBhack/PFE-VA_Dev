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


    def __init__(self, port, frequency=MISC.SOCKETS["frequency"]):
        """
            Initialization
        """
        self._port = port
        self._frequency = frequency
        self._connexions = []
        self._clientsListeningThreads = []
        self.alive = True

        self.waitForClient = True

    def set_sending_datagram(self, datagram):
        self._sendingDatagram = Message.Message(datagram)

    def set_receiving_datagram(self, datagram):
        self._receivingDatagram = Message.Message(datagram)

    def set_up_connexion(self, timeout=MISC.SOCKETS["timeout"], multiClients=False, maxClients=2):
        """
            Connexion set-up method
            Arguments :
                - timeout : the amount of time the server waits
                for something to happen before raising an error
                - multiClients
        """
        socket.setdefaulttimeout(timeout)

        newSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        newSocket.bind(('', self._port))
        newSocket.listen(1)

        clientsConnected = 0
        socketCreationTime = time.time()

        while self.waitForClient:
            try:
                newConnexion, _ = newSocket.accept()
                self._connexions.append({"sock": newConnexion, "stopEvent":threading.Event()})
                clientsConnected += 1
                if clientsConnected >= maxClients or not multiClients:
                    print('Maximum amount of clients reached (', clientsConnected, ')')
                    self.waitForClient = False
                if time.time() - socketCreationTime > timeout:
                    print("Timeout : ", clientsConnected, " clients connected")
                    self.waitForClient = False
            except KeyboardInterrupt:
                print("Interrupt received, stopping…")
                self.close()
            except socket.timeout:
                print("Timeout : ", clientsConnected, " clients connected")
                self.waitForClient = False

        if clientsConnected > 0:
            print("Success !")

    def listen_to_clients(self, callback, args):
        """
            Listening to clients Method
        """
        for connexion in self._connexions:
            self._clientsListeningThreads.append(WaitForData(connexion, self._receivingDatagram, callback, args, self._frequency, self.close_single_socket))
            self._clientsListeningThreads[-1].start()

    def send_to_clients(self, data):
        """
            Send to clients Method
        """
        for connexion in self._connexions:
            try:
                connexion["sock"].send(self._sendingDatagram.encode(data))
            except (ConnectionResetError, BrokenPipeError):
                self.close_single_socket(connexion)

    def close_single_socket(self, connexion):
        connexion["stopEvent"].set()
        time.sleep(0.01)
        connexion["sock"].close()
        self._connexions.remove(connexion)
        print("Connection closed by client.", str(len(self._connexions)), " client(s) remaining.")
        if len(self._connexions) <= 0:
            print("All clients disconnected. Closing the server.")
            try:
                connexion["sock"].shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.alive = False

    def close(self):
        self.waitForClient = False
        for connexion in self._connexions:
            connexion["stopEvent"].set()
            time.sleep(0.01)
            try:
                connexion["sock"].shutdown(socket.SHUT_RDWR)
            except:
                pass
            connexion["sock"].close()
            self._connexions.remove(connexion)
            print('Closing')
            self.alive = False
        #for thread in self._clientsListeningThreads:
        #    thread.join()

class WaitForData(threading.Thread):
    """
        WaitForData Class (threading)
    """

    def __init__(self, connexion, datagram, callback, args, frequency, closeMethod):
        """
            Initialization
        """
        threading.Thread.__init__(self)
        self.connexion = connexion
        self._datagram = datagram
        self._messageSize = datagram.size
        self.callback = callback
        self._args = args
        self._frequency = frequency
        self._closeMethod = closeMethod        

    def run(self):
        """
            Running (when start is called)
        """
        while not self.connexion["stopEvent"].is_set():
            try:
                data = self.connexion["sock"].recv(self._messageSize)
                if data:
                    self.callback(self._datagram.decode(data), self._args)
            except ConnectionResetError:
                self._closeMethod(self.connexion)
