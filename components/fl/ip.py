import numpy as np
import cv2
import sys
import atexit

###Specific imports :
##robotBasics:
from robotBasics.constants.connectionSettings import IP as IP_CS
from robotBasics.constants.misc import IP as IP_MISC
#Classes & Methods:
from robotBasics.sockets.tcp.Server import Server as Server
from robotBasics.logger import robotLogger
##Adafruit_BBIO:
import Adafruit_BBIO.GPIO as GPIO

LOOKFOR = 0 #0 = RED, 1 = GREEN


#If we are on an actual robot :
if path.isdir("/home/robot"):
    ROBOT_ROOT = '/home/robot'
elif path.isfile(path.expanduser('~/.robotConf')):
    #If we're not on an actual robot, check if we have
    #a working environment set for robot debugging:
    ROBOT_ROOT = open(path.expanduser('~/.robotConf'), 'r').read().strip().close()

    #Simulator setup
    GPIO.pin_association(RESET_GPIO, 'pushbutton\'s state')
    GPIO.setup_behavior('print')
else:
    ROBOT_ROOT = ''
    print('It seems like you are NOT working on an actual robot. \
You should set up a debugging environment before running any code (see documentation)')

#Logging Initialization :
LOGGER = robotLogger("FL > pb", ROBOT_ROOT+'logs/fl/')


#######################################################################
#                    CONSTANTS FOR IMAGE PROCESSING                   #
#######################################################################
BOUNDARIES = [[[255, 150, 237], [161, 87, 159]], [[70, 141, 255], [23, 44, 138]]]
ERODE = 1
DILATE = 3
KERNEL_SIZE = 0
MINCIRCLESIZE = 2
MAXCIRCLESIZE = 17
KERNEL = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

#######################################################################
#                     SERVERS SET UP AND SETTINGS :                   #
#######################################################################

#### SERVER CONNECTION :

#Creating the connection object
SERVER = Server(IP_CS, LOGGER)
#Registering the close method to be executed at exit (clean deconnection)
atexit.register(SERVER.close)

#Opening the connection
SERVER.connect()

#### CALLBACKS' ARGUMENT SETUP:

ARGUMENTS = {
    "connection" : SERVER
}

###########################################################################
#                               RUNNING :                                 #
###########################################################################

#Waiting for requests and linking them to the callback method
SERVER.listen_to_clients(light_send_state, ARGUMENTS)

def light_send_state(data, arg):
    arg["connection"].send_to_clients(checking_exectutor())

CAP = cv2.VideoCapture(1)
_ = CAP.set(3, 320)
_ = CAP.set(4, 240)

RET, FRAME = CAP.read()
height, width,channels = FRAME.shape

MINYLOCATION = 1
MINXLOCATION = width/2
MAXYLOCATION = height
MAXXLOCATION = width

def checking_exectutor():
    retry = 0
    error = True

    isGreen = 0
    isRed = 0

    while retry < IP_MISC['max_retry']:
    # ^ = Xor, means either Green or Red MUST be on.
        isRed = check_light_color(0)
        isGreen = check_light_color(1)
        if isRed ^ isGreen:
            error=False
            break
        retry = retry + 1
    
    return [error, isRed]   
    


def check_light_color(LOOKFOR):
    #Red (LOOKFOR=0) and green (LOOKFOR=1)
    finalCirclesArray = []

    #Get image
    RET, FRAME = CAP.read()

    #Convert to HSV color space
    _HSV = cv2.cvtColor(FRAME, cv2.COLOR_BGR2HSV)

    lower = np.array(BOUNDARIES[LOOKFOR][1])
    upper = np.array(BOUNDARIES[LOOKFOR][0])

    # If pixel HSV values are between boundaries, then mask pixel = 1 else 0
    MASK = cv2.inRange(_HSV, lower, upper)

    ERODED = cv2.erode(MASK, KERNEL, iterations=ERODE) #Erosion : remove noise, "little"
    ERODED_AND_DILATED = cv2.dilate(ERODED, KERNEL, iterations=DILATE) #Dilatation : enlarge the interesting area

    HSVcol = cv2.bitwise_and(_HSV, _HSV, mask=ERODED_AND_DILATED) # Apply mask to HSV frame

    CNTS = cv2.findContours(ERODED_AND_DILATED, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2] #Find rough contours

    for i in CNTS:
        (tx, ty), tradius = cv2.minEnclosingCircle(i)
        x = int(tx)
        y = int(ty)
        radius = int(tradius)

        if radius >= MINCIRCLESIZE and radius <= MAXCIRCLESIZE and\
        x > MINXLOCATION and x < MAXXLOCATION and\
        y > MINYLOCATION and y < MAXYLOCATION :
            finalCirclesArray.append([x,y,radius])      

    if len(finalCirclesArray)==1:
        fileName = str(time.strftime("%Y%m%d-%H%M%S", time.localtime())) + "_"
        fileName = filename + "GREEN" if LOOKFOR else "RED"
        fileName = filename + "jpg"
        cv2.imwrite(fileName,FRAME)
        return 1
    else:
        return 0

def exit():
    CAP.release()
    cv2.destroyAllWindows()
