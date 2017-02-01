import numpy as np
import cv2
from tkinter import *
import os.path
import time

DEBUG = True
USE_CAMERA = True

SIZE = 320

LOOKFOR = 0 #0 = RED, 1 = GREEN

indent = ""
class GUI():
    def __init__(self,XMAX, YMAX):
        self.GUIvar = Tk()

        colorChoiceFrame = Frame(self.GUIvar)
        colorChoiceFrame.pack()

        allScales = Frame(self.GUIvar)
        allScales.pack()
        greenScales = Frame(allScales, relief=SUNKEN)
        greenScales.pack(side = LEFT)
        redScales = Frame(allScales)
        redScales.pack()
        processScales = Frame(allScales, relief=SUNKEN)
        processScales.pack(side = BOTTOM)

        self.LOOKFOR = 0
        self.actualBounds = StringVar()
        self.value = IntVar()
        self.RED_SELECT = Radiobutton(colorChoiceFrame, text="Rouge", variable=self.value, value=0, command=self.GetLookfor)
        self.GREEN_SELECT = Radiobutton(colorChoiceFrame, text="Vert", variable=self.value, value=1, command=self.GetLookfor)
        self.BOTH = Radiobutton(colorChoiceFrame, text="TOUTES", variable=self.value, value=2, command=self.GetLookfor)

        self.HUPG   = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper H')
        self.HUPG.set(255)
        self.SUPG   = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper S')
        self.SUPG.set(255)
        self.VUPG   = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper V')
        self.VUPG.set(255)
        self.HDOWNG = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower H')
        self.SDOWNG = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower S')
        self.VDOWNG = Scale(greenScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower V')

        self.HUPR   = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper H')
        self.HUPR.set(255)
        self.SUPR   = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper S')
        self.SUPR.set(255)
        self.VUPR   = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Upper V')
        self.VUPR.set(255)
        self.HDOWNR = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower H')
        self.SDOWNR = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower S')
        self.VDOWNR = Scale(redScales, orient='horizontal', from_=0, to=255, resolution=1, length=200, label='Lower V')

        self.ERODE  = Scale(self.GUIvar, orient='horizontal', from_=0, to=10, resolution=1, length=200, label='Erode factor')
        self.DILATE = Scale(self.GUIvar, orient='horizontal', from_=0, to=10, resolution=1, length=200, label='Dilatation factor')
        self.KERNEL_SIZE = Scale(self.GUIvar, orient='horizontal', from_=0, to=10, resolution=1, length=100, label='Kernel size')

        self.GENERATE = Button(self.GUIvar, text="Generate", command=self.makePy)
        self.GENERATE.pack()
        self.BOUNDARIES = Entry(self.GUIvar, textvariable=self.actualBounds)
        self.BOUNDARIES.pack(side = TOP, fill=X)

        self.MAXCIRCLESIZE = Scale(self.GUIvar, orient='horizontal', from_=0, to=50, resolution=1, length=200, label='Max Circle Size')
        self.MINCIRCLESIZE = Scale(self.GUIvar, orient='horizontal', from_=0, to=50, resolution=1, length=200, label='Min Circle Size')
        self.MAXCIRCLESIZE.pack()
        self.MINCIRCLESIZE.pack()

        self.boundariesFrame = Tk()
        self.MINYLOCATION = Scale(self.boundariesFrame, orient='vertical', from_=1, to=YMAX-1, resolution=1, length=200, label='Min y location')
        self.MINXLOCATION = Scale(self.boundariesFrame, orient='horizontal', from_=1, to=XMAX-1, resolution=1, length=200, label='Min x location')
        self.MAXYLOCATION = Scale(self.boundariesFrame, orient='vertical', from_=1, to=YMAX, resolution=1, length=200, label='Max y location')
        self.MAXXLOCATION = Scale(self.boundariesFrame, orient='horizontal', from_=1, to=XMAX, resolution=1, length=200, label='Max x location')
        self.MINYLOCATION.pack(side=LEFT)
        self.MINXLOCATION.pack()
        self.MAXYLOCATION.pack(side=LEFT)
        self.MAXXLOCATION.pack()

        self.RED_SELECT.pack(side = LEFT)
        self.GREEN_SELECT.pack(side = LEFT)
        self.BOTH.pack(side=LEFT)

        self.HUPG.pack()
        self.SUPG.pack()
        self.VUPG.pack() 
        self.HDOWNG.pack()
        self.SDOWNG.pack()
        self.VDOWNG.pack()

        self.HUPR.pack()
        self.SUPR.pack()
        self.VUPR.pack() 
        self.HDOWNR.pack()
        self.SDOWNR.pack()
        self.VDOWNR.pack()

        self.ERODE.pack(side = LEFT) 
        self.DILATE.pack(side = LEFT)
        self.KERNEL_SIZE.pack(side = LEFT)


    def GetLookfor(self):
        self.LOOKFOR = self.value.get()

    def makePy(self):
        i = 0
        
        if os.path.isfile("trafficLight.py"):
            file = open("trafficLight.py", "r")
            lines = file.readlines()
            for line in lines:
                if line[:10]=='BOUNDARIES':
                    break
                i = i + 1
            file.close()
            lines[i] = "BOUNDARIES = " + self.actualBounds.get() + "\n"
            lines[i+1] = "ERODE = " + str(self.ERODE.get()) + "\n"
            lines[i+2] = "DILATE = " + str(self.DILATE.get()) + "\n"
            lines[i+3] = "KERNEL_SIZE = " + str(self.KERNEL_SIZE.get()) + "\n"
            file = open("trafficLight.py", "w")

            for line in lines:
                file.write("%s" % line)
            file.close()
            print("DONE !")

    def update(self):
        self.printBoundaries()
        self.GUIvar.update()
        self.boundariesFrame.update()

    def printBoundaries(self):
        newBounds = [[[self.HUPG.get(), self.SUPG.get(), self.VUPG.get()],[self.HDOWNG.get(), self.SDOWNG.get(), self.VDOWNG.get()]],[[self.HUPR.get(), self.SUPR.get(), self.VUPR.get()],[self.HDOWNR.get(), self.SDOWNR.get(), self.VDOWNR.get()]]]
        newBoundsStr = str(newBounds)
        if not newBoundsStr == self.actualBounds.get():
            self.actualBounds.set(newBoundsStr)

def nothing(_):
    """ createTrackbar feedback -- UNUSED"""

CAP = cv2.VideoCapture(1)
_ = CAP.set(3, SIZE)
_ = CAP.set(4, SIZE * 0.75)

RET, FRAME = CAP.read()
# FRAME = cv2.imread('trafficLightTest.jpg')
height,width,channels = FRAME.shape
print("Height : " + str(height) + "\tWidth : " + str(width))
guiObj = GUI(width,height)   
guiObj.update()

while True:

    RET, FRAME = CAP.read()
    # FRAME = cv2.imread('trafficLightTest.jpg')

    HUPG = guiObj.HUPG.get()
    SUPG = guiObj.SUPG.get()
    VUPG = guiObj.VUPG.get()

    WHATTODETECT = guiObj.LOOKFOR
    if WHATTODETECT == 2:
        LOOKFOR = 1 - LOOKFOR
    else:
        LOOKFOR = WHATTODETECT
    
    #LOOKFOR = 1 - LOOKFOR

    HDOWNG = guiObj.HDOWNG.get()
    SDOWNG = guiObj.SDOWNG.get()
    VDOWNG = guiObj.VDOWNG.get()

    HUPR = guiObj.HUPR.get()
    SUPR = guiObj.SUPR.get()
    VUPR = guiObj.VUPR.get()

    HDOWNR = guiObj.HDOWNR.get()
    SDOWNR = guiObj.SDOWNR.get()
    VDOWNR = guiObj.VDOWNR.get()

    ERODE = guiObj.ERODE.get()
    DILATE = guiObj.DILATE.get()

    MAXCIRCLESIZE = guiObj.MAXCIRCLESIZE.get()
    MINCIRCLESIZE = guiObj.MINCIRCLESIZE.get() 

    MINYLOCATION = guiObj.MINYLOCATION.get()
    MINXLOCATION = guiObj.MINXLOCATION.get()
    MAXYLOCATION = guiObj.MAXYLOCATION.get()
    MAXXLOCATION = guiObj.MAXXLOCATION.get()

    if MINYLOCATION >= MAXYLOCATION:
        MINYLOCATION = MAXYLOCATION - 1
    if MINXLOCATION >= MAXXLOCATION:
        MINXLOCATION = MAXXLOCATION - 1

    KERNEL_SIZE = guiObj.KERNEL_SIZE.get()
    KERNEL = np.ones((KERNEL_SIZE, KERNEL_SIZE), np.uint8)

    _HSV = cv2.cvtColor(FRAME, cv2.COLOR_BGR2HSV)

    #BOUNDARIES = [[[HUPG, SUPG, VUPG],[HDOWNG, SDOWNG, VDOWNG]],[[HUPR, SUPR, VUPR],[HDOWNR, SDOWNR, VDOWNR]]]
    BOUNDARIES = [[[255, 255, 255],[0, 20, 255]],[[72, 0, 255],[0, 0, 229]]]
    ERODE = 0    
    DILATE = 2
    MAXCIRCLESIZE = 10
    MINCIRCLESIZE = 2

    lower = np.array(BOUNDARIES[LOOKFOR][1])
    upper = np.array(BOUNDARIES[LOOKFOR][0])

    MASK = cv2.inRange(_HSV, lower, upper)

    ERODED = cv2.erode(MASK, KERNEL, iterations=ERODE)
    ERODED_AND_DILATED = cv2.dilate(ERODED, KERNEL, iterations=DILATE)

    HSVcol = cv2.bitwise_not(_HSV, _HSV, mask=ERODED_AND_DILATED)


    TMP = ERODED_AND_DILATED.copy()
    CNTS = cv2.findContours(TMP, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    cv2.drawContours(ERODED_AND_DILATED, CNTS, -1, (255, 255, 255), -1)
    HSVcol = cv2.bitwise_and(_HSV, _HSV, mask=ERODED_AND_DILATED)

    # if len(CNTS) == 0:
    #     pass
    # else:
    #     indent = indent + "-"
    #     if len(indent) == 15:
    #         indent = ""
    #     if LOOKFOR == 0:
    #         print(indent + "TRAFFIC LIGHT IS RED")
    #     if LOOKFOR == 1:
    #         print(indent + "TRAFFIC LIGHT IS GREEN")       
    
    DEBUGSCREEN = FRAME
    VIEW = FRAME[MINYLOCATION:MAXYLOCATION,MINXLOCATION:MAXXLOCATION]
    finalCirclesArray = []

    for i in CNTS:
        (tx, ty), tradius = cv2.minEnclosingCircle(i)
        x = int(tx)
        y = int(ty)
        radius = int(tradius)

        if radius >= MINCIRCLESIZE and radius <= MAXCIRCLESIZE and\
        x > MINXLOCATION and x < MAXXLOCATION and\
        y > MINYLOCATION and y < MAXYLOCATION :
            finalCirclesArray.append([x,y,radius])
            cv2.circle(DEBUGSCREEN, (x, y), radius, (0, 255, 0), 2)

    if len(finalCirclesArray)==1:
        print("GREEN" if LOOKFOR else "RED")

    cv2.imshow('frame', FRAME)
    cv2.imshow('ERODED_AND_DILATED', ERODED_AND_DILATED)
    cv2.imshow('hsvcol', HSVcol)
    cv2.imshow('Debug', DEBUGSCREEN)
    cv2.imshow('mask', MASK)
    cv2.imshow('Searching region', VIEW)

    guiObj.update()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# When everything done, release the CAPture
CAP.release()
cv2.destroyAllWindows()

