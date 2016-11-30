"""
    Connection Settings constants for inter-modules communication
"""

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

US = {
    "port": 49250,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

IP = {
    "port": 49260,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": [['BITS', [1, 1]]]
                #First bit  : Traffic light detected
                #Second bit : 0 = Red, 1 = Green
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

PBC = {
    "port": 49310,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

QE = {
    "port": 49320,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['FLOAT']
    }
}

USC = {
    "port": 49330,
    "datagrams": {
        "clientToServer": ['BOOL'],
        "serverToClient": ['BOOL']
    }
}

VSC = {
    "velocity": {
        "port": 49340,
        "datagrams": {
            "clientToServer": ['SMALL_INT_SIGNED'],
            "serverToClient": ['SMALL_INT_SIGNED']
        }
    },
    "steering": {
        "port": 49341,
        "datagrams": {
            "clientToServer": ['SMALL_INT_SIGNED'],
            "serverToClient": ['SMALL_INT_SIGNED']
        }
    }
}

# Decision Level (DL)

VE = {
    "velocity": {
        "port": 49400,
        "datagrams": {
            "clientToServer": ['SMALL_INT_SIGNED'],
            "serverToClient": ['BOOL']
        }
    },
    "oa": {
        "port": 49401,
        "datagrams": {
            "clientToServer": ['BOOL'],
            "serverToClient": ['BOOL']
        }
    }
}
