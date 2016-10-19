"""
    mot.py
    Waits for a description of the desired state for the two motors,
    deduces and apply the appropriate PWM and responds with a
    notification when the request has been fulfilled.
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import atexit

#Specific imports :
import robotBasics as RB
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

#Documentation : https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
MOTOR_LEFT = RB.constants.gpiodef.ENGINES["left"]
MOTOR_RIGHT = RB.constants.gpiodef.ENGINES["right"]

#Start PWM with a 0% duty cycle
PWM.start(MOTOR_LEFT["PWM"], 0)
PWM.start(MOTOR_RIGHT["PWM"], 0)

#Declare motor enabling pins
########### NOTE ############
# To go forward  : set forward  pin to 1 and backward pin to 0
# To go backward : set backward pin to 1 and forward  pin to 0
GPIO.setup(MOTOR_LEFT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_LEFT["backward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["backward"], GPIO.OUT)

#Set emabeling pins to LOW
GPIO.output(MOTOR_LEFT["forward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["forward"], GPIO.LOW)
GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def set_pwm_motor_left_cb(data, args):
    """
        Callback function for left motor :
        When instructions are updated through a request to the
        server, deduces and apply the corresponding motor configuration
    """

    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 and dutyCycle <= 100), "PWM must be set between -100 and 100"
    #Positive duty cycle = go forward
    if dutyCycle >= 0:
        GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_LEFT["forward"], GPIO.HIGH)
    #Negative duty cycle = go backward
    else:
        GPIO.output(MOTOR_LEFT["forward"], GPIO.LOW)
        GPIO.output(MOTOR_LEFT["backward"], GPIO.HIGH)
    #Setting the duty cycle
    PWM.set_duty_cycle(MOTOR_LEFT["PWM"], abs(dutyCycle))

    #Inform the client that is request have been fulfilled.
    args["connection"].send_to_clients([True])

def set_pwm_motor_right_cb(data, args):
    """
        Callback function for right motor :
        When instructions are updated through a request to the
        server, deduces and apply the corresponding motor configuration
    """
    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 and dutyCycle <= 100), "PWM must be set between -100 and 100"
    #Positive duty cycle = go forward
    if dutyCycle >= 0:
        GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_RIGHT["forward"], GPIO.HIGH)
    #Negative duty cycle = go backward
    else:
        GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_RIGHT["forward"], GPIO.HIGH)
    #Setting the duty cycle
    PWM.set_duty_cycle(MOTOR_RIGHT["PWM"], abs(dutyCycle))

    #Inform the client that is request have been fulfilled.
    args["connection"].send_to_clients([True])

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

SOCKETS = RB.sockets

#### SERVER CONNECTION :

#Creating the TCP instances
CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["mot"]["left"])
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["mot"]["right"])
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(CONNECTION_MOTOR_LEFT.close)
atexit.register(CONNECTION_MOTOR_RIGHT.close)

#We'll send booleans (status of the operation)
CONNECTION_MOTOR_LEFT.set_sending_datagram(['BOOL'])
CONNECTION_MOTOR_RIGHT.set_sending_datagram(['BOOL'])

#We'll receive small signed integers (-100 -> 100% of thrust)
CONNECTION_MOTOR_LEFT.set_receiving_datagram(['SMALL_INT_SIGNED'])
CONNECTION_MOTOR_RIGHT.set_receiving_datagram(['SMALL_INT_SIGNED'])

#Opening the connection
CONNECTION_MOTOR_LEFT.set_up_connection(600)
CONNECTION_MOTOR_RIGHT.set_up_connection(600)

#Arguments object for the callback method
#We pass the CONNECTION object so that the callback can respond to the request
ARGUMENTS_MOTOR_LEFT = {
    "connection" : CONNECTION_MOTOR_LEFT
}

ARGUMENTS_MOTOR_RIGHT = {
    "connection" : CONNECTION_MOTOR_RIGHT
}

#Waiting for requests and redirecting them to the callback method
CONNECTION_MOTOR_LEFT.listen_to_clients(set_pwm_motor_left_cb, ARGUMENTS_MOTOR_LEFT)
CONNECTION_MOTOR_RIGHT.listen_to_clients(set_pwm_motor_right_cb, ARGUMENTS_MOTOR_RIGHT)
