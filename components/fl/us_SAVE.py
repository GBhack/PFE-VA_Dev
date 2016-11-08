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

"""
def measure_distance_cb(data, arg):
    """
        #Callback method
        #Called when a tcp request is received
        #Trigger an ultrasonic measure and sends back the echo time in seconds
    """
    startTime = 0
    stopTime = 0

    while startTime ==0 and stopTime == 0:

        time.sleep(0.01)
        initTime = time.time()

        GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.HIGH)
        GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

        while not GPIO.input(RB.constants.gpiodef.SONAR["echo"]) and initTime-time.time() < 1:
            startTime = time.time()

        while GPIO.input(RB.constants.gpiodef.SONAR["echo"]) and initTime-time.time() < 1:
            stopTime = time.time()

    duration = stopTime - startTime
    distance = round(duration * 343.2 / 2, 3)
    #print("Distance: " + str(distance) + "m")
    arg["connection"].send_to_clients([distance])
"""

def obstacle_detection_cb(data, arg):
    obstacleDetected = False
    if GPIO.input(RB.constants.gpiodef.SONAR["echo"]):
         obstacleDetected = True
    arg["connection"].send_to_clients([obstacleDetected])

#GPIO setup :
GPIO.setup(RB.constants.gpiodef.SONAR["trigger"], GPIO.OUT)
GPIO.setup(RB.constants.gpiodef.SONAR["echo"], GPIO.IN)

GPIO.output(RB.constants.gpiodef.SONAR["trigger"], GPIO.LOW)

SOCKETS = RB.sockets

#Creating the connection object
CONNECTION = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["us"])
print(RB.constants.ports.FL["us"])

#We'll send bool
CONNECTION.set_sending_datagram(['BOOL'])

#We'll receive booleans (request)
CONNECTION.set_receiving_datagram(['BOOL'])

#Opening the connection
CONNECTION.set_up_connection(10)

#Arguments object for the callback method
#We pass the CONNECTION object so that the callback can respond to the request
ARGUMENTS = {
    "connection" : CONNECTION
}

#Waiting for requests and linking them to the callback method
CONNECTION.listen_to_clients(measure_distance_cb, ARGUMENTS)


atexit.register(CONNECTION.close)