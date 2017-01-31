from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger

OS = {
    "port": 49210,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

LOGGER = robotLogger("test", '')

SERVER = Server(OS, LOGGER)

SERVER.connect()

SERVER.send([True])

