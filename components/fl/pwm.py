"""
    LF_PWM.py
    Handles the PWM generation
"""

#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

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

# def set_settings_cb(data, arg):
#     """ 
#         This method handles the input arguments
#         It ensures that the input args are correct and redirect to appropriate method
#     """
#     if arg[0] == "pwmMotorLeft" or arg[0] == "pwmMotorRight":
#         pwmValue = arg[1]
#         try:
#             if pwmValue < 0 or pwmValue > 100:
#                 raise ValueError

#             if arg[0] == "pwmMotorLeft":
#                 set_pwm_motor_left(pwmValue)
#             elif arg[0] == "pwmMotorRight":
#                 set_pwm_motor_right(pwmValue)

#         except ValueError:
#             print('The required value is a percentage and must be between 0 and 100\n')
#             print('Setting everything to 0 duty cycle\n')
#             set_pwm_motor_left(0)
#             set_pwm_motor_right(0)
#             raise
#         except Exception:
#             raise
#     elif arg[0] == "setFrequency":
#         set_frequency(arg[1])
#     elif arg[0] == "setPeriod":
#         set_period(arg[1])
#     else:
#         print('Invalid argument : unknown method ' + arg[0])


def set_pwm_motor_left(dutyCycle):
    """
        Set the pwm duty cycle of the left motor
    """
    PWM.set_duty_cycle(MOTOR_LEFT["PWM"], dutyCycle)

def set_pwm_motor_right(dutyCycle):
    """
        Set the pwm duty cycle of the right motor
    """
    PWM.set_duty_cycle(MOTOR_RIGHT["PWM"], dutyCycle)


SOCKETS = RB.sockets

CONNEXION_MOTOR_RIGHT = SOCKETS.udp.Client.Client(RB.constants.ports.FL["pwm_right"])
print(CONNEXION_MOTOR_RIGHT.receive_data())
