"""
    Message.py
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import math
from . import Packet

class Message(object):
    """
        Message Class
    """

    def __init__(self, datagram):
        """
            Initialization
        """
        _messageSize = 0
        self.messageSize = 0

        self.packets = []


        for data in datagram:

            self.packets.append(Packet.Packet(data))
            _messageSize += int(self.packets[-1].get_size()/8)

        #If the packet size is not a power of two :
        if _messageSize != 0 and  (_messageSize & (_messageSize - 1)) != 0:
            _nextPowerOfTwo = math.ceil(math.log2(_messageSize))
            _nextPowerOfTwo = int(math.pow(2, _nextPowerOfTwo))
            _fillingSize = _messageSize - _nextPowerOfTwo
            self.packets.append(Packet.Packet(['FILLER', _fillingSize]))
            _messageSize = _nextPowerOfTwo
        self.messageSize = _messageSize

    def get_size(self):
        """
            get_size method
            Returns the size of the message
        """
        return self.messageSize

    def encode(self, dataset):
        """
            Datagran encoding (to bytes)
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

