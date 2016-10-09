#robotBasics > sockets > dataHandling
Modules dedicated to the data-handling part of socket communication (encoding and decoding, formatting...)<br />

In order to be able to flexibly exchange data while complying to sockets requirements, we adopted a system based on Messages composed of Packets :<br />

A Message is what is actually sent and received through the socket.
A message is an array of raw bytes (Bytes object in Python). A message must have a size being a power of two bytes.
So, if the total size of the packets composing the message is not a power of two, the packet will be completed with zeros until it reaches the next power of two.


A packet is an actual piece of data.
A packet can represent :
- An integer :
	- SMALL (0-255 unsigned, -127-127 signed) : 1 byte
	- MEDIUM (0-65535 unsigned, -32767-32767 signed) : 2 bytes
	- LARGE (0 4.29E9 unsigned -2.14E9-2.14E9 signed) : 4 bytes
	All integers are big-endians
- A floating point number on 4 bytes
- A boolean (0 will be False and 1 will be True)
- A raw byte
- An array of bits :<br />
	Must be declared as a list like this : ['BITS', [sizeOfBlock1, sizeOfBlock2, ...]]<br />
	Then can be used to send unsigned integers.<br />
	No size limit.<br />
	For instance : ['BITS', [1,1,2,4,2]] can be used to pack [0,1,3,11,2] or [1,0,2,5,1] but not [2,3,4,53,5]<br />

Packets allways weigh bytes. A packet cannot be 10 bits long : it will be filled to be 16 bits (2 bytes) long.<br />
<br />
So, on the sending side, we can create a Message object like this :
```
sendingMessage = Message(['SMALL_INT_UNSIGNED', 'FLOAT', 'BOOL', ['BITS',[1,1,2]] ])
```
Then we can use this object to pack data we want to sent :
```
dataToSend = sendingMessage.encode([212, 3.141593, True, [1,0,2]])
```
So we have :
```
dataToSend = b'\xdc\x0fI@'
dataToSend = ['0xd4', '0xdc', '0x0f', '0x49', '0x40', '0x01', '0x09']
dataToSend = [1101 0100, 1101 1100, 0000 1111, 0100 1001, 0100 0000, 0000 0001, 0000 1001]
             |   212   |              0.3141593....                |  True    |  1,0,10  |
```
