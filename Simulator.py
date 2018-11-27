# Updated Animation Starter Code
import time
from createStuff import *
from tkinter import *
from PIL import ImageTk,Image  
from roads import *
from sideRoads import *
from intersections import * 
####################################
# customize these functions
####################################

def init(data):
    data.yellowTime = 1
    data.roads = []
    #intersecs is a dictionary with keys = tuple of intersection location and 
    #value = intersections. this way you can look up if an intersection 
    #already exists  
    data.intersecs = {}

    #drawing out your custom intersections
    data.increment = 20
    data.tmpStartX = 0
    data.tmpStartY = 0
    data.tmpEndX = data.tmpStartX
    data.tmpEndY = data.tmpStartY
    #only start when user done with drawing when they press space
    data.go = False
    data.tmpDir = None
    
    #timer
    data.t = 0
    
    data.yellowLightImg = PhotoImage(file="imgs/yellowLight.gif")
    data.redLightImg = PhotoImage(file="imgs/redLight.gif")
    data.greenLightImg = PhotoImage(file="imgs/greenLight.gif")

    data.intersecRad = 40
        #center of the intersection
    data.intersecX = data.width//2
    data.intersecY = data.height//2
    
    data.intersecRad = 40
    
def mousePressed(event, data):
    mousePressedC (event, data)
def avgTimeSpentWaiting ():
    return SideIntersection.totalTimeWaiting/SideIntersection.totalCars

def keyPressed(event, data):
    keyPressedC (event, data)
    if event.keysym == "d":
        print (SideIntersection.totalTimeWaiting)
        print (SideIntersection.totalCars)
        print (avgTimeSpentWaiting())

def timerFired(data):
    data.t += 1
    for road in data.roads:
        road.timerFiredRoad(data, time.time())
    for i in data.intersecs:
        data.intersecs[i].timerFiredIntersec (data)
    

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
    drawTmp (canvas, data)
    for road in data.roads:
        road.drawAllRoad(canvas, data)
    if data.go:
        for i in data.intersecs:
            data.intersecs[i].drawAllIntersec(data, canvas)

def setTheLights(lights):
    j = 0
    for i in data.intersecs:
        data.intersecs[i].NSTime = lights [j][0]
        data.intersecs[i].EWTime = lights [j][1]
        j += 1


####################################
# use the run function as-is
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

run(800, 800)