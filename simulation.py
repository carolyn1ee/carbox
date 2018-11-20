import tkinter
import random 
from image_util import *
from tkinter import *
import os
from carClass import *
from PIL import ImageTk,Image 

        ##for now just making the radius be the buffer (will use some math later to figure out the safe distance a car needs to be)
        


####################################
# customize these functions
####################################
("Downloads/000_cmu/cs/tp/imageCarWE")


def init(data):
    #amt of time in secs for the light to be green
    data.NSTime = 5
    data.EWTime = 5
    #interval of seconds between each car that enters
    data.EWCarRate = 5
    data.NSCarRate = 2
    data.WECarRate = 3
    data.SNCarRate = 4


     
    
    data.carsSN = []
    data.carsWE = []
    data.carsNS = []
    data.carsEW = []
    data.allCars = [data.carsSN, data.carsNS, data.carsEW, data.carsWE]
    #green light means 1 and red light means 0
    data.NS = 1
    data.EW = 0
    data.totTimeWaiting = 0
    data.t = 0
    data.radius = 20
    data.intersecRad = 40
    #center of the intersection
    data.intersecX = data.width//2
    data.intersecY = data.height//2

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass
    
    
    
    
    ######
####TIMER
    ######
#tells you if n seconds have passed
def timerIsNSecs (data, n):
    #timerFired goes off 10 times per sec
    firesPerSec = 10 
    return data.t % (firesPerSec * n) == 0
    
def inIntersection (data, car):
    return car.x < data.intersecX + data.intersecRad and car.x > data.intersecX - data.intersecRad and car.y < data.intersecY + data.intersecRad and car.y > data.intersecY - data.intersecRad 
    
def moveCarsInList (l):
    for car in l:
        car.move()
        
def decelCarsInList(data, l):
    for car in l:
        car.deceler()
            
def timerFired(data):
    data.t += 1
    firesPerSec = 10 
#will change the hardcoded values later to be in some random range for the acceleration and the speed when creating new car objects
    if timerIsNSecs (data, data.NSTime):
        car = Car (data, 10, [0,1], 1,1)
        data.carsNS += [car]
    if timerIsNSecs (data, data.SNCarRate):
        car = Car (data, 10, [0,-1], 1, 1)
        data.carsSN += [car]
    if timerIsNSecs (data, data.EWCarRate):
        car = Car (data, 10,[-1,0], 1,1)
        data.carsEW += [car]
    if timerIsNSecs (data, data.WECarRate):
        car = Car (data, 10,[1,0], 1,1)
        data.carsWE += [car]
    for l in data.allCars:
        moveCarsInList(l)
    
    for carList in [data.carsNS, data.carsSN, data.carsEW,\
    data.carsWE]:
        for c in range(1, len(carList)):
            if carList[c].isTooClose(carList[c-1]):
                print (c)
                carList[c].deceler()
                print (carList[c].curSpeed)
    
    
    if not data.NS:
        #slow down the cars if red or orange light
        for car in data.carsNS:
            if inIntersection (data, car):
                decelCarsInList (data, data.carsNS)
        for car in data.carsSN:
            if inIntersection (data, car):
                decelCarsInList (data, data.carsSN)
        
    if not data.EW:
        for car in data.carsEW:
            if inIntersection (data, car):
                car.deceler()
                car.curSpeed = 0
        for car in data.carsWE:
            if inIntersection (data, car):
                car.deceler()
                car.curSpeed = 0
    
    ####
## view
    ####

def drawCarsInList (canvas, data, l):
    #from https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python: image syntax
    ####WHY NO HAVE MULTIPLE CARS!??!?
    for car in l:
        #print (car.img)
        #data.img = PhotoImage(file="imageCarWE.gif")
        #canvas.create_image(car.x, car.y, image=data.img) 
        canvas.create_oval(car.x - data.radius, car.y -data.radius, car.x +data.radius, car.y+data.radius)

        
def stopLightColor (light):
    if light == 1:
        return 'green'
    elif light == 0: 
        return 'red'
    else:
        return 'yellow'
        
def redrawAll(canvas, data):
     
    drawCarsInList (canvas,data, data.carsNS)
    drawCarsInList (canvas,data, data.carsSN)
    drawCarsInList (canvas,data, data.carsEW)
    drawCarsInList (canvas,data, data.carsWE)


    
    stopLightR = 8
    canvas.create_oval (data.width // 2 - stopLightR, \
            data.height // 2- 50 - stopLightR, \
            data.width // 2 + stopLightR,\
            data.height // 2 -50 + stopLightR, \
            fill = stopLightColor(data.NS))
    
    canvas.create_oval (data.width // 2 - 50 - stopLightR, \
        data.height // 2 - stopLightR, \
        data.width // 2 - 50 + stopLightR, \
        data.height // 2 + stopLightR, \
        fill = stopLightColor (data.EW))
    

####################################
# use the run function as-is
#cite: from course website
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)
    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    root.resizable(width=False, height=False) # prevents resizing window
    init(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)
