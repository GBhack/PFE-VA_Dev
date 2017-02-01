import atexit
import time
from os import path

###Specific imports :
##robotBasics:
#Constants:
from robotBasics.constants.connectionSettings import LEDC as LEDC_CS
from robotBasics.constants.gpiodef import LEDS_ID as LEDS_ID
#Classes & Methods:
from robotBasics.sockets.tcp.Client import Client as Client
from robotBasics.logger import robotLogger
LOGGER = robotLogger("FL > led", '')
LEDS_CLIENT = Client(LEDC_CS, LOGGER)

#Opening the connection
LEDS_CLIENT.connect()

for i in range(10):
    LEDS_CLIENT.send([[LEDS_ID["STOP"], bool(i%2)]])
    time.sleep(1)
