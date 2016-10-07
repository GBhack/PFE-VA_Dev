"""
    us.py
    Fonctionnal Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    If a request is received, triggers an ultrasound on the
    HC-SR04 and responds with the echo time in seconds
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO
import time

def measure_distance_cb(data, arg):
    """
        Callback method
        Called when a tcp request is received
        Trigger an ultrasonic measure and sends back the echo time in seconds
    """

    #GPIO setup :
    GPIO.setup(RB.gpiodef.SONAR["trigger"], GPIO.OUT)
    GPIO.setup(RB.gpiodef.SONAR["echo"], GPIO.IN)

    #Waiting for the sonar to initialize
    time.sleep(0.05)

    #Triggering :
    GPIO.output(RB.gpiodef.SONAR["trigger"], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(RB.gpiodef.SONAR["trigger"], GPIO.LOW)

    #Waiting for the echo pin to be "high" (echo start)
    while not GPIO.input(RB.gpiodef.SONAR["echo"]):
        startTime = time.time()
    #Waiting for the echo pin to be "low" (echo stop)
    while GPIO.input(RB.gpiodef.SONAR["echo"]):
        endTime = time.time()

    #Computing echo duration
    duration = endTime - startTime

    #Responding to the request with the echo duration
    arg["connexion"].send_to_clients([duration])




SOCKETS = RB.sockets

#Creating the connexion object
CONNEXION = SOCKETS.tcp.Server.Server(12345)

#We'll send floats (duration in seconds)
CONNEXION.set_sending_datagram(['FLOAT'])
#We'll receive booleans (request)
CONNEXION.set_receiving_datagram(['BOOL'])

#Opening the connexion
CONNEXION.set_up_connexion()

#Arguments object for the callback method
#We pass the CONNEXION object so that the callback can respond to the request
ARGUMENTS = {
    "connexion" : CONNEXION
}

#Waiting for requests and linking them to the callback method
CONNEXION.listen_to_clients(measure_distance_cb, ARGUMENTS)


#TCP.close()
