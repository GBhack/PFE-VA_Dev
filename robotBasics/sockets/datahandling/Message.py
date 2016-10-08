"""
    Message.py
    Define the Message class.
    We call "message" the data transmitted through sockets.
    A message is composed of "packets" (see Packet.py)
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import math

#Specific imports :
from . import Packet

class Message(object):
    """
        Message Class
        A message is a set of packets (see documentation)
    """

    def __init__(self, datagramPattern):
        """
            Initialization Method
            ARGUMENTS :
            - datagramPattern : The pattern of the datagram, as a list (see documentation)
        """

        #The global size of the message (in bytes)
        self._messageSize = 0

        #List of the packets composing the message (as Packet objects : see class definition)
        self.packets = []

        #For each distinct packet in the datagram pattern list
        for data in datagramPattern:

            self.packets.append(Packet.Packet(data))
            self._messageSize += int(self.packets[-1].get_size()/8)

        #If the packet size is not a power of two :
        if (self._messageSize != 0 and
                (self._messageSize & (self._messageSize - 1)) != 0):

            _nextPowerOfTwo = math.ceil(math.log2(self._messageSize))
            _nextPowerOfTwo = int(math.pow(2, _nextPowerOfTwo))
            _fillingSize = self._messageSize - _nextPowerOfTwo
            self.packets.append(Packet.Packet(['FILLER', _fillingSize]))
            self._messageSize = _nextPowerOfTwo

    def get_size(self):
        """
            get_size method
            Returns the size of the message in bytes
        """
        return self._messageSize

    def encode(self, dataset):
        """
            Datagran encoding (to bytes)
            Encode the whole dataset into a bytes array that can be transmitted
            through socket according to the datagram structure
            ARGUMENTS :
            - dataset : The set of data we want to encode (must be compliant
            with the datagram pattern provided during initialization)
        """
        _output = bytes()
        for index, packet in enumerate(self.packets):
            if packet.get_type() != 'FILLER':
                _output += packet.encode(dataset[index])
            else:
                _output += packet.encode(1)

        return _output

    def decode(self, dataset):
        """
            Datagran decoding (from bytes)
        """
        _output = []

        for packet in self.packets:
            _blockSize = int(packet.get_size()/8)
            if packet.get_type() != 'FILLER':
                _block = dataset[:_blockSize]
                dataset = dataset[_blockSize:]
                _output.append(packet.decode(_block))

        return _output

