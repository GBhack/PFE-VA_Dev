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

def compute_distance_cb(data, arg):
    """
        Callback method
        Called when a tcp request is received
        Trigger an ultrasonic measure through us (fl) and sends back the
        frontal distance in meters.
    """

    #Triggering :
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

    #Waiting for the echo pin to be "high" (echo start)
    while not GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
        startTime = time.time()
    #Waiting for the echo pin to be "low" (echo stop)
    while GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
        endTime = time.time()

    #Computing echo duration
    duration = endTime - startTime

    #Responding to the request with the echo duration
    arg["connexion"].send_to_clients([duration])


SOCKETS = RB.sockets

#Creating the connexion object
SERVER = SOCKETS.tcp.Server.Server(RB.constants.ports.ECL["gfd"])

#We'll send floats (distance in meters)
SERVER.set_sending_datagram(['FLOAT'])
#We'll receive booleans (request)
SERVER.set_receiving_datagram(['BOOL'])

#Opening the connexion
SERVER.set_up_connexion()


#Creating the connexion object
CLIENT = SOCKETS.tcp.Server.Client(RB.constants.ports.FL["us"])

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
