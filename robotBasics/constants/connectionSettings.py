#Functionnal Level (FL) :

LED = {
    "port": 49200,
    "datagrams": {
        "clientToServer": [['BITS', [1, 1, 1, 1]]],
        "serverToClient": ["BOOL"]
    }
}

MOT_BASICS = {
    "port": 49210,
    "datagrams": {
        "clientToServer": ['SMALL_INT_SIGNED'],
        "serverToClient": ["BOOL"]
    }
}

MOT = {
    "LEFT": {},
    "RIGHT": {}
}

MOT["LEFT"] = dict(MOT_BASICS)
MOT["RIGHT"] = dict(MOT_BASICS)
MOT["RIGHT"]["port"] += 1


OS = {
    "port": 49220,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": [['BITS', [1, 1, 1, 1, 1, 1, 1]]]
    }
}

PB = {
    "port": 49230,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

QE = {
    "port": 49240,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['MEDIUM_INT_UNSIGNED']
    }
}

PB = {
    "port": 49250,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

#Execution Control Level (ECL):

LEDC = {
    "port": 49300,
    "datagrams": {
        "clientToServer": [['BITS', [2, 1]]],
        "serverToClient": ["BOOL"]
    }
}