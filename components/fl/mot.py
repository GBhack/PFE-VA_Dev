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


#Documentation : https://learn.adafruit.com/setting-up-io-python-library-on-beaglebone-black/pwm
MOTOR_LEFT = RB.constants.gpiodef.ENGINES["left"]
MOTOR_RIGHT = RB.constants.gpiodef.ENGINES["right"]

#Start PWM with a 0% duty cycle
#PWM.start(MOTOR_LEFT["PWM"], 0)
#PWM.start(MOTOR_RIGHT["PWM"], 0)
GPIO.setup(MOTOR_LEFT["PWM"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["PWM"], GPIO.OUT)
GPIO.output(MOTOR_LEFT["PWM"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["PWM"], GPIO.LOW)

#Declare motor enabling pins
########### NOTE ############
# To go forward  : set forward  pin to 1 and backward pin to 0
# To go backward : set backward pin to 1 and forward  pin to 0
GPIO.setup(MOTOR_LEFT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_LEFT["backward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["backward"], GPIO.OUT)

#Enable motors (active HIGH) : forward configuration
GPIO.output(MOTOR_LEFT["forward"], GPIO.HIGH)
GPIO.output(MOTOR_RIGHT["forward"], GPIO.HIGH)
GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)


def set_pwm_motor_left_cb(data, args):
    """
        Set the pwm duty cycle of the left motor
    """
    
    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 and dutyCycle <= 100), "PWM must be set between -100 and 100"
    if dutyCycle >= 0:
        GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_LEFT["forward"], GPIO.HIGH)
        print("LEFT direction : low")
        #GPIO.output(MOTOR_LEFT["direction"], GPIO.LOW)
    else:
        GPIO.output(MOTOR_LEFT["forward"], GPIO.LOW)
        GPIO.output(MOTOR_LEFT["backward"], GPIO.HIGH)
        print("LEFT direction : high")
        #GPIO.output(MOTOR_LEFT["direction"], GPIO.HIGH)
    print("LEFT PWM : " + str(abs(dutyCycle)))
    #PWM.set_duty_cycle(MOTOR_LEFT["PWM"], abs(dutyCycle))
    #
    #
    #
    #
    if dutyCycle > 0 :
        GPIO.output(MOTOR_LEFT["PWM"], GPIO.HIGH)
    else:
        GPIO.output(MOTOR_LEFT["PWM"], GPIO.LOW)





    args["connection"].send_to_clients([True])

def set_pwm_motor_right_cb(data, args):
    """
        Set the pwm duty cycle of the right motor
    """
    assert (data), "No data"
    dutyCycle = data[0]
    assert (dutyCycle >= -100 and dutyCycle <= 100), "PWM must be set between -100 and 100"
    if dutyCycle >= 0:
        GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_RIGHT["forward"], GPIO.HIGH)
        print("RIGHT direction : low")
        #GPIO.output(MOTOR_RIGHT["direction"], GPIO.LOW)
    else:
        GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)
        GPIO.output(MOTOR_RIGHT["forward"], GPIO.HIGH)
        print("RIGHT direction : high")
        #GPIO.output(MOTOR_RIGHT["direction"], GPIO.HIGH)
    print("RIGHT PWM : " + str(abs(dutyCycle)))
    #PWM.set_duty_cycle(MOTOR_RIGHT["PWM"], abs(dutyCycle))
    #
    #
    #
    #
    if dutyCycle > 0 :
        GPIO.output(MOTOR_RIGHT["PWM"], GPIO.HIGH)
    else:
        GPIO.output(MOTOR_RIGHT["PWM"], GPIO.LOW)
    args["connection"].send_to_clients([True])


SOCKETS = RB.sockets

#Creating the connection object
CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["mot"]["left"])
atexit.register(CONNECTION_MOTOR_LEFT.close)
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Server.Server(RB.constants.ports.FL["mot"]["right"])
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

#Waiting for requests and linking them to the callback method
CONNECTION_MOTOR_LEFT.listen_to_clients(set_pwm_motor_left_cb, ARGUMENTS_MOTOR_LEFT)
CONNECTION_MOTOR_RIGHT.listen_to_clients(set_pwm_motor_right_cb, ARGUMENTS_MOTOR_RIGHT)
