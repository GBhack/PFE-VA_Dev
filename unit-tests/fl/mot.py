"""
    mot.py
    TEST SCRIPT !
    For motors testing

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import time


#Specific imports :
from robotBasics.constants import gpiodef as GPIODEF
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM as PWM


"""
####################################################
#               Simulator setup                    #
####################################################

GPIO.pin_association(GPIODEF.ENGINES["left"]["PWM"], 'left motor\'s PWM')
GPIO.pin_association(GPIODEF.ENGINES["right"]["PWM"], 'right motor\'s PWM')
PWM.pin_association(GPIODEF.ENGINES["left"]["forward"], 'left motor\'s forward pin')
PWM.pin_association(GPIODEF.ENGINES["right"]["forward"], 'right motor\'s forward pin')
PWM.pin_association(GPIODEF.ENGINES["left"]["backward"], 'left motor\'s backward pin')
PWM.pin_association(GPIODEF.ENGINES["right"]["backward"], 'right motor\'s backward pin')
GPIO.setup_behavior('print')
PWM.setup_behavior('print')
"""

####################################################
#                     I/O setup                    #
####################################################

PWM.start(GPIODEF.ENGINES["left"]["PWM"], 0, 500)
PWM.start(GPIODEF.ENGINES["right"]["PWM"], 0, 500)

GPIO.setup(GPIODEF.ENGINES["left"]["forward"], GPIO.OUT)
GPIO.output(GPIODEF.ENGINES["left"]["forward"], GPIO.LOW)
GPIO.setup(GPIODEF.ENGINES["left"]["backward"], GPIO.OUT)
GPIO.output(GPIODEF.ENGINES["left"]["backward"], GPIO.LOW)
GPIO.setup(GPIODEF.ENGINES["right"]["forward"], GPIO.OUT)
GPIO.output(GPIODEF.ENGINES["right"]["forward"], GPIO.LOW)
GPIO.setup(GPIODEF.ENGINES["right"]["backward"], GPIO.OUT)
GPIO.output(GPIODEF.ENGINES["right"]["backward"], GPIO.LOW)


#Forward:
GPIO.output(GPIODEF.ENGINES["left"]["forward"], GPIO.HIGH)
GPIO.output(GPIODEF.ENGINES["right"]["forward"], GPIO.HIGH)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 10)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 10)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 20)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 20)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 30)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 30)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 40)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 40)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 50)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 50)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 70)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 70)
time.sleep(5)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 50)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 50)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 20)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 20)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 0)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 0)

time.sleep(5)

#Backward:
GPIO.output(GPIODEF.ENGINES["left"]["forward"], GPIO.LOW)
GPIO.output(GPIODEF.ENGINES["right"]["forward"], GPIO.LOW)
GPIO.output(GPIODEF.ENGINES["left"]["backward"], GPIO.HIGH)
GPIO.output(GPIODEF.ENGINES["right"]["backward"], GPIO.HIGH)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 10)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 10)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 20)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 20)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 30)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 30)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 40)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 40)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 50)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 50)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 70)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 70)
time.sleep(5)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 50)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 50)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 20)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 20)
time.sleep(0.2)
PWM.set_duty_cycle(GPIODEF.ENGINES["left"]["PWM"], 0)
PWM.set_duty_cycle(GPIODEF.ENGINES["right"]["PWM"], 0)
