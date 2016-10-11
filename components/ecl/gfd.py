"""
    gfd.py
    Execution Control Level module : Get Frontal Distance
    Waits for a TCP request on its own port
    When gets a request, sends a request to the us module (fl)
    and responds to the first request with the computed frontal distance
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Specific imports :
import robotBasics as RB

CONSTANTS = RB.constants

def compute_distance_cb(data, arg):
    """
        Callback method
        Called when a tcp request is received
        Trigger an ultrasonic measure through us (fl) and sends back the
        frontal distance in meters.
    """

    distance = data * 343.2 / 2
    arg['CLIENT'].send_data(distance)

SOCKETS = RB.sockets

#Creating the connexion object
SERVER = SOCKETS.tcp.Server.Server(CONSTANTS.ports.ECL["gfd"])

#We'll send floats (distance in meters)
SERVER.set_sending_datagram(['FLOAT'])
#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connexion
SERVER.set_up_connexion()


#Creating the connexion object
CLIENT = SOCKETS.tcp.Client.Client(CONSTANTS.ports.FL["us"])

#We'll send floats (distance in meters)
CLIENT.set_sending_datagram(['BOOL'])
#We'll receive booleans (request)
CLIENT.set_receiving_datagram(['FLOAT'])

#Opening the connexion
CLIENT.set_up_connexion()

#Arguments object for the callback method
#We pass the CONNEXION object so that the callback can respond to the request
ARGUMENTS = {
    "SERVER" : SERVER,
    "CLIENT" : CLIENT
}

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(compute_distance_cb, ARGUMENTS)


#TCP.close()
