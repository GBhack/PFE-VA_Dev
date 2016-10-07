"""
    fl_us.py
    Fonctionnal Level module : Ultrasonic Sensor manager
"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO
import time

def measure_distance(data, arg):
    """
        Callback method for printing a message
    """
    GPIO.setup(RB.gpiodef.SONAR["trigger"], GPIO.OUT)
    GPIO.setup(RB.gpiodef.SONAR["echo"], GPIO.IN)

    time.sleep(0.05)

    GPIO.output(RB.gpiodef.SONAR["trigger"], GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(RB.gpiodef.SONAR["trigger"], GPIO.LOW)

    while not GPIO.input(RB.gpiodef.SONAR["echo"]):
        startTime = time.time()
    while GPIO.input(RB.gpiodef.SONAR["echo"]):
        endTime = time.time()

    duration = endTime - startTime

    distance = duration * 171.5

    arg["connexion"].send_to_clients([distance])




SOCKETS = RB.sockets

CONNEXION = SOCKETS.tcp.Server.Server(12345)

CONNEXION.set_sending_datagram(['FLOAT'])
CONNEXION.set_receiving_datagram(['BOOL'])

CONNEXION.set_up_connexion()

ARGUMENTS = {
    "connexion" : CONNEXION
}

CONNEXION.listen_to_clients(measure_distance, ARGUMENTS)


#TCP.close()
