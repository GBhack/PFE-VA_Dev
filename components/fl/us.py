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
import atexit
import time

#Specific imports :
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO

def measure_distance_cb(data, arg):
    """
        Callback method
        Called when a tcp request is received
        Trigger an ultrasonic measure and sends back the echo time in seconds
    """
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.HIGH)
    GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

    while not GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
        startTime = time.time()

    while GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
        stopTime = time.time()

    duration = stopTime - startTime
    print("Echo duration : " + str(duration))
    arg["connexion"].send_to_clients([duration])


#GPIO setup :
GPIO.setup(RB.constants.gpiodef.SONAR["trigger"], GPIO.OUT)
GPIO.setup(RB.constants.gpiodef.SONAR["echo"], GPIO.IN)

GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

SOCKETS = RB.sockets

#Creating the connexion object
CONNEXION = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["us"])
print(RB.constants.ports.FL["us"])

#We'll send bool
CONNEXION.set_sending_datagram(['FLOAT'])

#We'll receive booleans (request)
CONNEXION.set_receiving_datagram(['BOOL'])

#Opening the connexion
CONNEXION.set_up_connection(10)

#Arguments object for the callback method
#We pass the CONNEXION object so that the callback can respond to the request
ARGUMENTS = {
    "connexion" : CONNEXION
}

#Waiting for requests and linking them to the callback method
CONNEXION.listen_to_clients(measure_distance_cb, ARGUMENTS)


atexit.register(CONNEXION.close)
