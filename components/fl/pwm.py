"""
    LF_PWM.py
    Handles the PWM generation
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

def init():
    #Documentation : https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
    motorLeft = RB.gpiodef.ENGINES["left"]
    motorRight = RB.gpiodef.ENGINES["right"]

    #Start PWM with a 0% duty cycle
    pwmMotorLeft = PWM.start(motorLeft["PWM"], 0)
    pwmMotorRight = PWM.start(motorRight["PWM"], 0)
    
    #Declare motor enabling pins
    GPIO.setup(motorLeft["enable"], GPIO.OUT)
    GPIO.setup(motorRight["enable"], GPIO.OUT)

    #Declare direction pins
    GPIO.setup(motorLeft["direction"], GPIO.OUT)
    GPIO.setup(motorRight["direction"], GPIO.OUT)

    #Enable motors (active HIGH)
    GPIO.output(motorLeft["direction"], GPIO.HIGH)
    GPIO.output(motorRight["direction"], GPIO.HIGH)

    #Initialize direction
    # LOW = Forward
    # HIGH = Backward
    GPIO.output(motorLeft["direction"], GPIO.LOW)
    GPIO.output(motorRight["direction"], GPIO.LOW)


def set_pwm(data, arg):




SOCKETS = RB.sockets

CONNEXION = SOCKETS.tcp.Server.Server(RB.ports.FL["pwm"])
CONNEXION.set_sending_datagram(['BOOL'])
CONNEXION.set_receiving_datagram(['BYTE'])
CONNEXION.set_up_connexion()

ARGUMENTS = {
    "connexion" : CONNEXION
}

init()

CONNEXION.listen_to_clients(set_pwm, ARGUMENTS)