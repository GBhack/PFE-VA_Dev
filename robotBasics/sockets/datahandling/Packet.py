"""
    Packet.py
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import math

class Packet(object):
    """
        Packet Class
    """


    def __init__(self, description):
        """
            Initialization
        """
        _knowTypes = ['INT', 'FLOAT', 'BOOL', 'BYTE', 'BITS', 'FILLER']
        _knownDefinitions = ['SMALL', 'MEDIUM', 'LARGE']
        _knownSigning = ['SIGNED', 'UNSIGNED']

        _type = 'OTHER'
        _definition = 'OTHER'
        _signing = 'UNSIGNED'

        try:
            assert not isinstance(description, str)
            _type = description[0]
            _detail = description[1]

        except AssertionError:
            try:
                _definition, _type, _signing = description.split('_')
            except ValueError:
                try:
                    _definition, _type = description.split('_')
                except ValueError:
                    _type = description


        if _type not in _knowTypes:
            raise ValueError('Unknown type : '+_type)

        self.type = _type

        if _type == 'INT':

            if  _definition not in _knownDefinitions:
                raise ValueError('Unknown definition : '+_definition)
            if _signing not in _knownSigning:
                raise ValueError('Unknown signing type : '+_signing)

            if _definition == 'SMALL':
                self.size = 8
            elif _definition == 'MEDIUM':
                self.size = 16
            elif _definition == 'LARGE':
                self.size = 32
        elif _type == 'FLOAT':
            self.size = 32
        elif _type in ['BOOL', 'BYTE']:
            self.size = 8
        elif _type == 'BITS':
            self.detail = _detail
            self.masks = []
            self.shift = []
            _bitsSize = sum(_detail)
            _complement = 8 - _bitsSize % 8
            self.size = _bitsSize + _complement
            _bits = 0
            for block in _detail:
                _mask = 0
                for i in range(0, block):
                    _mask += math.pow(2, i + _bits)
                self.shift.append(int(_bits))
                self.masks.append(int(_mask))
                _bits += block
        elif _type == 'FILLER':
            self.size = _detail



        if _signing == 'SIGNED':
            self.signed = True
            self.offset = pow(2, self.size-1)-1
        else:
            self.signed = False
            self.offset = 0

    def get_size(self):
        """
            get_size method
            Returns the size of the packet
        """
        return self.size

    def get_type(self):
        """
            get_type method
            Returns the type of the packet
        """
        return self.type

    def encode(self, data=1):
        """
            Datapiece encoding (to bytes)
        """

        if self.type == 'INT':
            if not self.signed:
                assert data >= 0
            data = int(data+self.offset)
            assert data < pow(2, self.size) and data >= 0
            return data.to_bytes(int(self.size/8), byteorder='big')
        elif self.type == 'BITS':
            assert len(data) == len(self.detail)
            _output = 0
            _bitsCount = 0
            for index, dataPiece in enumerate(data):
                assert dataPiece < math.pow(2, self.detail[index])
                _output += int(dataPiece * math.pow(2, _bitsCount))
                _bitsCount += self.detail[index]
            return _output.to_bytes(int(self.size/8), byteorder='big')
        elif self.type == 'FILLER':
            _output = int(math.pow(2, self.size) - 1)
            return _output.to_bytes(int(self.size/8), byteorder='big')
        elif self.type == 'FLOAT':
            from struct import pack
            print("FLOAT :")
            print(bytearray(pack('f', data)))
            return bytearray(pack('f', data))
        elif self.type == 'BOOL':
            assert data in [True, False, 0, 1]
            if data:
                return int(1).to_bytes(1, byteorder='big')
            else:
                return int(0).to_bytes(1, byteorder='big')
        elif self.type == 'BYTE':
            return data

    def decode(self, data):
        """
            Datapiece decoding (from bytes)
        """

        if self.type == 'INT':
            data = int.from_bytes(data, byteorder='big')
            data = int(data-self.offset)
            return data
        elif self.type == 'BITS':
            data = int.from_bytes(data, byteorder='big')
            _output = []
            for index, mask in enumerate(self.masks):
                _output.append((data & mask) >> self.shift[index])
            return _output
        elif self.type == 'FLOAT':
            from struct import unpack
            return unpack('f', data)[0]
        elif self.type == 'BOOL':
            data = int.from_bytes(data, byteorder='big')
            if data == 1:
                return True
            else:
                return False
        elif self.type == 'BYTE':
            return data