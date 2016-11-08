"""
    us.py
    Functional Level module : Ultrasonic Sensor manager
    Waits for a TCP request on its own port
    When gets a request, responds with the obstacle detection
    state (read through the Atitiny)

"""


#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import logging
from robotBasics import constants as CONSTANTS

###########################################################################
#                         LOGGER INITIALIZATION :                         #
###########################################################################

formatter = logging.Formatter("[%(asctime)s : %(funcName)s - %(module)s @ %(filename)s (%(levelname)s)] \t %(message)s")

handler_errors = logging.FileHandler("../errors.log", mode="a", encoding="utf-8")
handler_debug  = logging.FileHandler("../debug.log", mode="a", encoding="utf-8")

handler_errors.setFormatter(formatter)
handler_debug.setFormatter(formatter)

handler_errors.setLevel(logging.WARNING)
handler_debug.setLevel(logging.DEBUG)

logger = logging.getLogger("robot")

logger.setLevel(CONSTANTS.misc.LOGGING['level'])

logger.addHandler(handler_errors)
logger.addHandler(handler_debug)


logger.debug('Message de debug 1')
logger.error('Message d\'erreur 1')
logger.debug('Message de debug 2')
logger.info('Message d\'information 1')