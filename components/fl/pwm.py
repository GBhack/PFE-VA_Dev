"""
    pwm.py
    Handles the PWM generation
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Specific imports :
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM


#Documentation : https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
MOTOR_LEFT = RB.constants.gpiodef.ENGINES["left"]
MOTOR_RIGHT = RB.constants.gpiodef.ENGINES["right"]

#Start PWM with a 0% duty cycle
PWM.start(MOTOR_LEFT["PWM"], 0)
PWM.start(MOTOR_RIGHT["PWM"], 0)

#Declare motor enabling pins
GPIO.setup(MOTOR_LEFT["enable"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["enable"], GPIO.OUT)

#Declare direction pins
GPIO.setup(MOTOR_LEFT["direction"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["direction"], GPIO.OUT)

#Enable motors (active HIGH)
GPIO.output(MOTOR_LEFT["enable"], GPIO.HIGH)
GPIO.output(MOTOR_RIGHT["enable"], GPIO.HIGH)

#Initialize direction
# LOW = Forward
# HIGH = Backward
# # DEFAULT : Forward # #
GPIO.output(MOTOR_LEFT["direction"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["direction"], GPIO.LOW)

def set_pwm_motor_left(data, args):
    """
        Set the pwm duty cycle of the left motor
    """
    
    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 and dutyCycle <= 100), "PWM must be set between -100 and 100"
    if dutyCycle >= 0:
        GPIO.output(MOTOR_LEFT["direction"], GPIO.LOW)
    else:
        GPIO.output(MOTOR_LEFT["direction"], GPIO.HIGH)
    PWM.set_duty_cycle(MOTOR_LEFT["PWM"], abs(dutyCycle))
    arg["connexion"].send_to_clients([True])

def set_pwm_motor_right(data, args):
    """
        Set the pwm duty cycle of the right motor
    """
    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 or dutyCycle <= 100), "PWM must be set between -100 and 100"
    if dutyCycle >= 0:
        GPIO.output(MOTOR_RIGHT["direction"], GPIO.LOW)
    else:
        GPIO.output(MOTOR_RIGHT["direction"], GPIO.HIGH)

    PWM.set_duty_cycle(MOTOR_RIGHT["PWM"], abs(dutyCycle))
    arg["connexion"].send_to_clients([True])


SOCKETS = RB.sockets

#Creating the connexion object
CONNEXION_MOTOR_LEFT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["pwm"]["left"])
CONNEXION_MOTOR_RIGHT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["pwm"]["right"])

#We'll send booleans (status of the operation)
CONNEXION_MOTOR_LEFT.set_sending_datagram(['BOOL'])
CONNEXION_MOTOR_RIGHT.set_sending_datagram(['BOOL'])

#We'll receive small signed integers (-100 -> 100% of thrust)
CONNEXION_MOTOR_LEFT.set_receiving_datagram(['SMALL_INT_SIGNED'])
CONNEXION_MOTOR_RIGHT.set_receiving_datagram(['SMALL_INT_SIGNED'])

#Opening the connexion
CONNEXION_MOTOR_LEFT.set_up_connexion()
CONNEXION_MOTOR_RIGHT.set_up_connexion()

#Arguments object for the callback method
#We pass the CONNEXION object so that the callback can respond to the request
ARGUMENTS_MOTOR_LEFT = {
    "connexion" : CONNEXION_MOTOR_LEFT
}

ARGUMENTS_MOTOR_RIGHT = {
    "connexion" : CONNEXION_MOTOR_RIGHT
}

#Waiting for requests and linking them to the callback method
CONNEXION_MOTOR_RIGHT.listen_to_clients(set_pwm_motor_left, ARGUMENTS_MOTOR_LEFT)
CONNEXION_MOTOR_RIGHT.listen_to_clients(set_pwm_motor_right, ARGUMENTS_MOTOR_RIGHT)
