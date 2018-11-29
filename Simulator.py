# Updated Animation Starter Code
import time
from createStuff import *
from tkinter import *
from PIL import ImageTk,Image  
from roads import *
from sideRoads import *
from intersections import * 
from startScreen import *

#framework from cs website
def init(data, roads, intersecs, set):
    data.yellowTime = 1
    data.roads = roads
    #intersecs is a dictionary with keys = tuple of intersection location and 
    #value = intersections. this way you can look up if an intersection 
    #already exists  
    data.intersecs = intersecs

    #drawing out your custom intersections
    data.increment = 20
    data.tmpStartX = 0
    data.tmpStartY = 0
    data.tmpEndX = data.tmpStartX
    data.tmpEndY = data.tmpStartY
    #only start when user done with drawing when they press space
    data.tmpDir = None
    
    data.tmpCar = None
    data.crashes = 0 #num times cars run into each other
    
    #timer
    data.t = 0
    
    
    data.yellowLightImg = PhotoImage(file="imgs/yellowLight.gif")
    data.redLightImg = PhotoImage(file="imgs/redLight.gif")
    data.greenLightImg = PhotoImage(file="imgs/greenLight.gif")

    # data.intersecRad = 40
    #     #center of the intersection
    # data.intersecX = data.width//2
    # data.intersecY = data.height//2
    # 
    data.intersecRad = 40
    
    data.set = set
    
    data.screen = "startScreen"
    #screen can also be "setScreen"
    
def mousePressed(event, data):
    if data.set:
        mousePressedC (event, data)
def avgTimeSpentWaiting ():
    if SideIntersection.totalCars == 0:
        return None
    return SideIntersection.totalTimeWaiting/SideIntersection.totalCars

def keyPressed(event, data):
    if data.set:
        if data.screen == "startScreen":
            keyPressedStart (event, data)
        elif data.screen == "setScreen":
            keyPressedC (event, data)
 
    # if event.keysym == "d":
    #     print (SideIntersection.totalTimeWaiting)
    #     print (SideIntersection.totalCars)
    #     print (avgTimeSpentWaiting())
    

def timerFired(data):
    if not data.set:
        data.t += 1
        for road in data.roads:
            # timer fires
            road.timerFiredRoad(data, time.time())
        for i in data.intersecs:
            data.intersecs[i].timerFiredIntersec (data)

        
        

def redrawAll(canvas, data):
    canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
    drawTmp (canvas, data)
    for road in data.roads:
        road.drawAllRoad(canvas, data)
    if data.screen == "startScreen" and data.set:
        redrawAllStart(canvas, data)
    if not data.set:
        for i in data.intersecs:
                data.intersecs[i].drawAllIntersec(data, canvas)

def setTheLights(data, lights):
    j = 0
    for i in data.intersecs:
        data.intersecs[i].NSTime = lights [j][0]
        data.intersecs[i].EWTime = lights [j][1]
        j += 1
    

####################################
# use the run function as-is
####################################

def run(set, width=300, height=300, lights = None, roads = [], intersecs = {}):
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
    data.timerDelay = 1 # milliseconds
    root = Tk()
    #syntax for the background color from https://stackoverflow.com/questions/2744795/background-color-for-tk-in-python
    root ["bg"] = "black"
    root.resizable(width=False, height=False) # prevents resizing window
    init(data, roads, intersecs, set)
    if not data.set:
        setTheLights(data, lights)
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
    # def destroy():
    #     #function to destroy window from https://stackoverflow.com/questions/8009176/function-to-close-the-window-in-tkinter
    #     root.destroy()
    root.quit()
  
    
    root.mainloop()  # blocks until window is closed
    if not data.set:
        return (SideIntersection.totalTimeWaiting, SideIntersection.totalCars, avgTimeSpentWaiting())
    else:
        replaceIntersections(data)
        return (data.roads, data.intersecs)
    print("bye!")

