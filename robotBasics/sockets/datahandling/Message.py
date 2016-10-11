"""
    Message.py
    Defines the Message class.
    We call "message" the data transmitted through sockets.
    A message is composed of "packets" (see Packet.py and directory's README)
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

    def __init__(self, messagePattern):
        """
            Initialization Method
            ARGUMENTS :
            - datagramPattern : The pattern of the datagram, as a list (see directory's README)
        """

        #The global size of the message (in bytes)
        self.size = 0

        #List of the packets composing the message (as Packet objects : see class definition)
        self.packets = []

        #For each distinct packet in the datagram pattern list
        for packetPattern in messagePattern:
            self.packets.append(Packet.Packet(packetPattern))
            self.size += int(self.packets[-1].size/8)

        #If the message size is not a power of two :
        if (self.size != 0 and
                (self.size & (self.size - 1)) != 0):
            #We compute the next power of two :
            _nextPowerOfTwo = math.ceil(math.log2(self.size))
            _nextPowerOfTwo = int(math.pow(2, _nextPowerOfTwo))
            #We compute the number of bytes missing to get a power of two
            _fillingSize = _nextPowerOfTwo - self.size
            #We "fill" the message to get a power of two size
            self.packets.append(Packet.Packet(['FILLER', _fillingSize]))
            self.size = _nextPowerOfTwo

    def encode(self, dataset):
        """
            Message encoding (to bytes)
            Encode the whole dataset into a bytes array that can be transmitted
            through socket according to the message's preset pattern
            ARGUMENTS :
            - dataset : The set of data we want to encode (must be compliant
            with the message's pattern provided during initialization)
        """
        #We create a byte array to store the result :
        _output = bytes()

        #For each packet composing the message :
        for index, packet in enumerate(self.packets):
            #If the packet contains user's data :
            if packet.type != 'FILLER':
                #We encode the user's data and add it to the output
                _output += packet.encode(dataset[index])
            #If the packet is a filler :
            else:
                _output += packet.encode(0)
        return _output

    def decode(self, rawData):
        """
            Message decoding (from bytes)
            Decode a byte array into a proper set of data according
            to the message's preset pattern
            ARGUMENTS :
            - rawData : The byte array we want to decode (must be compliant
            with the message's pattern provided during initialization)
        """
        _output = []
        _index = 0

        #For each packet of the message :
        for packet in self.packets:
            #We compute the backet size in bytes
            _packetSize = int(packet.size/8)

            #If the packet contains actual data :
            if packet.type != 'FILLER':
                #We "isolate" the packet from the whole message :
                _packetRawData = rawData[_index:_index+_packetSize]
                _index += _packetSize

                #We append the decoded packet to the output :
                _output.append(packet.decode(_packetRawData))

        return _output

