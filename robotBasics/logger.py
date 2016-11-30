#!/usr/bin/python3.5
#-*- coding: utf-8 -*-

#Standard imports :
import logging
from logging.handlers import RotatingFileHandler

class trimmingFormatter(logging.Formatter):
    def format(self, record):
        record.msg = record.msg.strip()
        record.msg = ' '.join(record.msg.split())
        return super(trimmingFormatter, self).format(record)

def robotLogger(caller, location = ''):
    formatter = trimmingFormatter("[%(asctime)s : "+caller+" > %(module)s @ %(filename)s :  %(funcName)s (%(levelname)s)] %(message)s")

    handler_errors = logging.handlers.RotatingFileHandler(location+"errors.log",
        mode="a", maxBytes = 100000, backupCount = 100, encoding="utf-8")
    handler_debug  = logging.handlers.RotatingFileHandler(location+"debug.log",
        mode="a", maxBytes = 100000, backupCount = 100, encoding="utf-8")
    handler_console = logging.StreamHandler()

    handler_errors.setFormatter(formatter)
    handler_debug.setFormatter(formatter)
    handler_console.setFormatter(formatter)

    handler_errors.setLevel(logging.WARNING)
    handler_debug.setLevel(logging.DEBUG)
    handler_console.setLevel(logging.INFO)

    logger = logging.getLogger("robot")

    logger.setLevel(logging.DEBUG)

    logger.addHandler(handler_errors)
    logger.addHandler(handler_debug)
    logger.addHandler(handler_console)

    return logger
