"""
    us.py
    Functional Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    When gets a request, triggers an ultrasound on the
    HC-SR04 and responds with the echo time in seconds
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time
import atexit

#Specific imports :
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO

def measure_distance_cb(data, arg):
    """
        Callback method
        Called when a tcp request is received
        Trigger an ultrasonic measure and sends back the echo time in seconds
    """
    global connexionInfo
    connexionInfo = arg
    
    print('Request received')

    #Triggering :
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

    print('Trigger signal sent. Now waiting for echo.')

    ##### DEPRECATED ####
    # #Waiting for the echo pin to be "high" (echo start)
    # while not GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
    #     startTime = time.time()
    # #Waiting for the echo pin to be "low" (echo stop)
    # while GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
    #     endTime = time.time()

    #Responding to the request with the echo duration

def echo_received_event():
    """
        Handles the echo receiving process
    """
    global connexionInfo
    if waitingForRisingEdge:    #If true, echo just received
        print('Echo received')
        startTime = time.time()
    else:                       #Means that echo ended
        print('Echo ended')
        connexionInfo["connexion"].send_to_clients([time.time() - startTime])

    waitingForRisingEdge = not waitingForRisingEdge # = waiting for falling edge
    

#GPIO setup :
GPIO.setup(RB.constants.gpiodef.SONAR["trigger"], GPIO.OUT)
GPIO.setup(RB.constants.gpiodef.SONAR["echo"], GPIO.IN)

# Using edge event for echo duration measurement
GPIO.add_edge_callback(RB.constants.gpiodef.SONAR["echo"], echo_received_event)

# Used in the echo_received_event callback function.
waitingForRisingEdge = True

SOCKETS = RB.sockets

#Creating the connexion object
CONNEXION = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["us"])
print(RB.constants.ports.FL["us"])

#We'll send floats (duration in seconds)
CONNEXION.set_sending_datagram(['FLOAT'])
#We'll receive booleans (request)
CONNEXION.set_receiving_datagram(['BOOL'])

#Opening the connexion
CONNEXION.set_up_connexion(10)

#Arguments object for the callback method
#We pass the CONNEXION object so that the callback can respond to the request
ARGUMENTS = {
    "connexion" : CONNEXION
}

#Waiting for requests and linking them to the callback method
CONNEXION.listen_to_clients(measure_distance_cb, ARGUMENTS)


atexit.register(CONNEXION.close)
