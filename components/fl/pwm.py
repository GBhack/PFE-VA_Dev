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
	motorLeft=RB.gpiodef.ENGINES["left"]
	GPIO.setup(motorLeft["PWM"], GPIO.OUT)
	GPIO.setup(motorLeft["direction"], GPIO.OUT)
	GPIO.setup(motorLeft["enable"], GPIO.OUT)

	motorRight=RB.gpiodef.ENGINES["right"]
	GPIO.setup(motorRight["PWM"], GPIO.OUT)
	GPIO.setup(motorRight["direction"], GPIO.OUT)
	GPIO.setup(motorRight["enable"], GPIO.OUT)


def set_pwm_motor_l(data, arg):


    time.sleep(0.05)
"""
PWM
direction
enable
"""
def set_pwm_motor_r(data, arg):


SOCKETS = RB.sockets

CONNEXION_PWM_MOTOR_L = SOCKETS.tcp.Server.Server(1110)
CONNEXION_PWM_MOTOR_L.set_sending_datagram(['BOOL'])
CONNEXION_PWM_MOTOR_L.set_receiving_datagram(['BYTE'])
CONNEXION_PWM_MOTOR_L.set_up_connexion()

ARGUMENTS_PWM_MOTOR_L = {
    "connexion" : CONNEXION_PWM_MOTOR_L
}

CONNEXION_PWM_MOTOR_R = SOCKETS.tcp.Server.Server(1120)
CONNEXION_PWM_MOTOR_R.set_sending_datagram(['BOOL'])
CONNEXION_PWM_MOTOR_R.set_receiving_datagram(['BYTE'])
CONNEXION_PWM_MOTOR_R.set_up_connexion()

ARGUMENTS_PWM_MOTOR_R = {
    "connexion" : CONNEXION_PWM_MOTOR_R
}

CONNEXION.listen_to_clients(set_pwm_motor_l, ARGUMENTS_PWM_MOTOR_L)
CONNEXION.listen_to_clients(set_pwm_motor_r, ARGUMENTS_PWM_MOTOR_R)

init()
