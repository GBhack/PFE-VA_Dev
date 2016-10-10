"""
    Packet.py
    Defines the Packet class.
    We call "packet" the data transmitted through sockets gathered inside Messages.
    The "packets" contains the actual data (see Packet.py and directory's README)
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import math

class Packet(object):
    """
        Packet Class
        A packet is an actual piece of data (see directory's README)
"""
    ###############################################
    #               INITIALIZATION                #
    ###############################################
    def __init__(self, description):
        """
            Initialization
        """

        #Only those types can be set at initialization :
        _knowTypes = ['INT', 'FLOAT', 'BOOL', 'BYTE', 'BITS', 'FILLER']

        #By default, we consider those attributes :
        self.type = 'OTHER'
        self.size = 0
        self._intAttr = {
            'definition':   'OTHER',
            'signing':      'UNSIGNED',
            'signed':       False,
            'offset':       0
        }

        self._bitsAttr = {
            'masks':     [],
            'shift':    []
        }

        #If the description is a list (for the type BITS or FILLING) :
        try:
            assert not isinstance(description, str)
            #We isolate the type from the detail :
            self.type = description[0]
            self._detail = description[1]
        #Else :
        except AssertionError:
            #If the definition and the signing method are given, we store them :
            try:
                self._intAttr['definition'], self.type, self._intAttr['signing'] = description.split('_')
            except ValueError:
                #If only the definition is given, we store it :
                try:
                    self._intAttr['definition'], self.type = description.split('_')
                except ValueError:
                    self.type = description

        #If the type is unknown, we raise an error :
        if self.type not in _knowTypes:
            raise ValueError('Unknown type : '+self.type)

        initializationMethod = {
            'INT': self._init_integer,
            'FLOAT': self._init_float,
            'BOOL': self._init_bool_byte,
            'BYTE': self._init_bool_byte,
            'BITS': self._init_bits,
            'FILLER': self._init_filler
        }

        initializationMethod[self.type]()


    def _init_integer(self):
        """
            Initialization method for integer type
        """

        #For an integer, those definitions can be declared :
        _knownDefinitions = ['SMALL', 'MEDIUM', 'LARGE']
        #For an integer, those signing methods can be declared :
        _knownSigning = ['SIGNED', 'UNSIGNED']

        if  self._intAttr['definition'] not in _knownDefinitions:
            raise ValueError('Unknown definition : '+self._intAttr['definition'])
        if self._intAttr['signing'] not in _knownSigning:
            raise ValueError('Unknown signing type : '+self._intAttr['signing'])

        if self._intAttr['definition'] == 'SMALL':
            self.size = 8
        elif self._intAttr['definition'] == 'MEDIUM':
            self.size = 16
        elif self._intAttr['definition'] == 'LARGE':
            self.size = 32

        if self._intAttr['signing'] == 'SIGNED':
            self._intAttr['signed'] = True
            self._intAttr['offset'] = pow(2, self.size-1)-1

    def _init_float(self):
        """
            Initialization method for float type
        """

        self.size = 32

    def _init_bool_byte(self):
        """
            Initialization method for boolean and byte type
        """

        self.size = 8

    def _init_bits(self):
        """
            Initialization method for bits type
        """

        _bitsSize = sum(self._detail)
        _complement = 8 - _bitsSize % 8
        self.size = _bitsSize + _complement
        _bits = 0
        for block in self._detail:
            _mask = 0
            for i in range(0, block):
                _mask += math.pow(2, i + _bits)
            self._bitsAttr['shift'].append(int(_bits))
            self._bitsAttr['masks'].append(int(_mask))
            _bits += block

    def _init_filler(self):
        """
            Initialization method for filler type
        """

        self.size = self._detail


    ###############################################
    #                  ENCODING                   #
    ###############################################
    def encode(self, data):
        """
            Packet encoding (to bytes)
        """
        encodingMethod = {
            'INT': self._encode_integer,
            'FLOAT': _encode_float,         #At the end of the file
            'BOOL': _encode_bool,           #At the end of the file
            'BYTE': _encode_byte,           #At the end of the file
            'BITS': self._encode_bits,
            'FILLER': self._encode_filler
        }

        return encodingMethod[self.type](data)


    def _encode_integer(self, data):
        """
            Encoding method for integer type
        """

        if not self._intAttr['signed']:
            assert data >= 0
        data = int(data+self._intAttr['offset'])
        assert data < pow(2, self.size) and data >= 0
        return data.to_bytes(int(self.size/8), byteorder='big')

    def _encode_bits(self, data):
        """
            Encoding method for bits type
        """

        assert len(data) == len(self._detail)
        _output = 0
        _bitsCount = 0
        for index, dataPiece in enumerate(data):
            assert dataPiece < math.pow(2, self._detail[index])
            _output += int(dataPiece * math.pow(2, _bitsCount))
            _bitsCount += self._detail[index]
        return _output.to_bytes(int(self.size/8), byteorder='big')

    def _encode_filler(self, _):
        """
            Encoding method for filler
        """

        _output = int(0).to_bytes(int(self.size), byteorder='big')
        return _output


    ###############################################
    #                   DECODING                  #
    ###############################################
    def decode(self, data):
        """
            Packet decoding (from bytes)
        """
        decodingMethod = {
            'INT': self._decode_integer,
            'FLOAT': _decode_float,         #At the end of the file
            'BOOL': _decode_bool,           #At the end of the file
            'BYTE': _decode_byte,           #At the end of the file
            'BITS': self._decode_bits
        }

        return decodingMethod[self.type](data)

    def _decode_integer(self, data):
        """
            Decoding method for integer type
        """

        data = int.from_bytes(data, byteorder='big')
        return int(data - self._intAttr['offset'])

    def _decode_bits(self, data):
        """
            Decoding method for bits type
        """

        data = int.from_bytes(data, byteorder='big')
        _output = []
        for index, mask in enumerate(self._bitsAttr['masks']):
            _output.append((data & mask) >> self._bitsAttr['shift'][index])
        return _output


####################################################
#                ENCODING  FUNCTIONS               #
####################################################
def _encode_float(data):
    """
        Encoding method for float type
    """

    from struct import pack
    return bytearray(pack('f', data))

def _encode_bool(data):
    """
        Encoding method for boolean type
    """

    assert data in [True, False, 0, 1]
    if data:
        return int(1).to_bytes(1, byteorder='big')
    else:
        return int(0).to_bytes(1, byteorder='big')

def _encode_byte(data):
    """
        Encoding method for byte type
    """

    try:
        data.decode()
        assert len(data) == 1
        return data
    except AttributeError:
        try:
            return int(data).to_bytes(1, byteorder='big')
        except:
            print('Error with BYTE. Are you sure to provide a single byte ?')


####################################################
#                DECODING  FUNCTIONS               #
####################################################
def _decode_byte(data):
    """
        Decoding method for byte type
    """
    return data

def _decode_bool(data):
    """
        Decoding method for boolean type
    """

    data = int.from_bytes(data, byteorder='big')
    return bool(data)

def _decode_float(data):
    """
        Decoding method for float type
    """

    from struct import unpack
    return unpack('f', data)[0]
