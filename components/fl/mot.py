"""
    mot.py
    Waits for a description of the desired state for the two motors,
    deduces and apply the appropriate PWM and responds with a
    notification when the request has been fulfilled.
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

###Standard imports :
import atexit

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants import gpiodef as GPIODEF
from robotBasics.constants.ports import FL as SERVER_PORTS
#Classes & Methods:
from robotBasics import sockets as SOCKETS
from robotBasics.logger import logger as LOGGER
##Adafruit_BBIO:
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM

"""
###########################################################################
#                             Simulator setup                             #
###########################################################################

PWM.pin_association(GPIODEF.ENGINES["left"]["PWM"], 'left motor\'s PWM')
PWM.pin_association(GPIODEF.ENGINES["right"]["PWM"], 'right motor\'s PWM')
GPIO.pin_association(GPIODEF.ENGINES["left"]["forward"], 'left motor\'s forward pin')
GPIO.pin_association(GPIODEF.ENGINES["right"]["forward"], 'right motor\'s forward pin')
GPIO.pin_association(GPIODEF.ENGINES["left"]["backward"], 'left motor\'s backward pin')
GPIO.pin_association(GPIODEF.ENGINES["right"]["backward"], 'right motor\'s backward pin')
GPIO.setup_behavior('print')
PWM.setup_behavior('print')
"""

###########################################################################
#                           I/O Initialization :                          #
###########################################################################

MOTOR_LEFT = GPIODEF.ENGINES["left"]
MOTOR_RIGHT = GPIODEF.ENGINES["right"]

#Start PWM with a 0% duty cycle
PWM.start(MOTOR_LEFT["PWM"], 0)
PWM.start(MOTOR_RIGHT["PWM"], 0)


#Declare motor enabling pins as outputs
GPIO.setup(MOTOR_LEFT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["forward"], GPIO.OUT)
GPIO.setup(MOTOR_LEFT["backward"], GPIO.OUT)
GPIO.setup(MOTOR_RIGHT["backward"], GPIO.OUT)

#Set enabeling pins to LOW
########### NOTE ############
# To go forward  : set forward  pin to 1 and backward pin to 0
# To go backward : set backward pin to 1 and forward  pin to 0
GPIO.output(MOTOR_LEFT["forward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["forward"], GPIO.LOW)
GPIO.output(MOTOR_LEFT["backward"], GPIO.LOW)
GPIO.output(MOTOR_RIGHT["backward"], GPIO.LOW)

###########################################################################
#                     Functions/Callbacks definition :                    #
###########################################################################

def set_pwm_cb(data, args):
    """
        Callback function motor controlling:
        When instructions are updated through a request to the
        server, deduces and apply the corresponding motor configuration
    """

    dutyCycle = data[0]
    if dutyCycle >= -100 and dutyCycle <= 100:
        message = 'Setting the '+args["name"]+' motor to go '
        #Positive duty cycle = go forward
        if dutyCycle >= 0:
            message += 'forward '

            GPIO.output(args["gpio"]["backward"], GPIO.LOW)
            GPIO.output(args["gpio"]["forward"], GPIO.HIGH)
        #Negative duty cycle = go backward
        else:
            message += 'backward '

            GPIO.output(args["gpio"]["forward"], GPIO.LOW)
            GPIO.output(args["gpio"]["backward"], GPIO.HIGH)

        message += 'with a PWM of '+str(abs(dutyCycle))
        #Setting the duty cycle
        PWM.set_duty_cycle(args["gpio"]["PWM"], abs(dutyCycle))

        #Inform the client that its request have been fulfilled.
        args["connection"].send_to_clients([True])

        LOGGER.debug(message)
    else:
        LOGGER.warning("PWM must be set between -100 and 100")
        LOGGER.debug("Incoherent command received. Keeping "+args["name"]+" motor in previous state.")
        #Inform the client that its request could not be fulfilled.
        args["connection"].send_to_clients([False])

###########################################################################
#                     CONNECTIONS SET UP AND SETTINGS :                   #
###########################################################################

#### SERVER CONNECTION :

#Creating the TCP instances
CONNECTION_MOTOR_LEFT = SOCKETS.tcp.Server.Server(SERVER_PORTS["mot"]["left"], LOGGER)
CONNECTION_MOTOR_RIGHT = SOCKETS.tcp.Server.Server(SERVER_PORTS["mot"]["right"], LOGGER)

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
    "connection" : CONNECTION_MOTOR_LEFT,
    "gpio" : MOTOR_LEFT,
    "name" : "left"
}

ARGUMENTS_MOTOR_RIGHT = {
    "connection" : CONNECTION_MOTOR_RIGHT,
    "gpio" : MOTOR_RIGHT,
    "name" : "right"
}

#Waiting for requests and redirecting them to the callback method
CONNECTION_MOTOR_LEFT.listen_to_clients(set_pwm_cb, ARGUMENTS_MOTOR_LEFT)
CONNECTION_MOTOR_RIGHT.listen_to_clients(set_pwm_cb, ARGUMENTS_MOTOR_RIGHT)
