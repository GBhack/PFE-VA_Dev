#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import logging
from logging.handlers import RotatingFileHandler

formatter = logging.Formatter("[%(asctime)s : %(funcName)s - %(module)s @ %(filename)s (%(levelname)s)] %(message)s")

handler_errors = logging.handlers.RotatingFileHandler("../errors.log", mode="a", maxBytes= 100000 , backupCount= 100 , encoding="utf-8")
handler_debug  = logging.handlers.RotatingFileHandler("../debug.log", mode="a", maxBytes= 100000 , backupCount= 100 , encoding="utf-8")

handler_errors.setFormatter(formatter)
handler_debug.setFormatter(formatter)

handler_errors.setLevel(logging.WARNING)
handler_debug.setLevel(logging.DEBUG)

logger = logging.getLogger("robot")

logger.setLevel(logging.DEBUG)

logger.addHandler(handler_errors)
logger.addHandler(handler_debug)