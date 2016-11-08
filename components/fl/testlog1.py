"""
    us.py
    Functional Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    When gets a request, responds with the obstacle detection
    state (read through the Atitiny)

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-
from robotBasics.logger import logger as LOGGER

LOGGER.debug('Message de debug 1')
LOGGER.error('Message d\'erreur 1')
LOGGER.debug('Message de debug 2')
LOGGER.info('Message d\'information 1')
LOGGER.warning('Message de warning 1')