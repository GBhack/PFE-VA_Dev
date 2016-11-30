from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.logger import robotLogger

OS = {
    "port": 49220,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

LOGGER = robotLogger("test", '')

CLIENT = Client(OS, LOGGER)

CLIENT.connect()

print(CLIENT.receive())
