# Updated Animation Starter Code from cs website
import time
from createStuff import *
from tkinter import *
from PIL import ImageTk,Image  
from roads import *
from sideRoads import *
from intersections import * 
from startScreen import *

#framework from cs website
def init(data, roads, intersecs, set, error, errorMsg):
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
    data.tmpDir = None
    data.rate = 4
    data.speedLim = 5
    
    data.tmpCar = None
    data.crashes = 0 #num times cars run into each other
    data.maxBack = 0
    data.weightBack = 1
    data.weightAvgWait = 1
    #timer
    data.t = 0
    
    #syntax for imgs from https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python and from course website
    # images from https://www.google.com/url?sa=i&source=images&cd=&cad=rja&uact=8&ved=2ahUKEwjuxora1YrfAhXvwVkKHQXDCOkQjRx6BAgBEAU&url=https%3A%2F%2Fpixabay.com%2Fen%2Ftraffic-light-yellow-traffic-lights-149582%2F&psig=AOvVaw02XfkJTMU_gd2fvVC1QYNd&ust=1544167324032447
    
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
    
    data.error = error
    data.errorMsg = errorMsg
    
def mousePressed(event, data):
    if data.set:
        mousePressedC (event, data)
def avgTimeSpentWaiting ():
    if SideIntersection.totalCars == 0:
        return None
    return SideIntersection.totalTimeWaiting/SideIntersection.totalCars
    
def curMaxBackup (data):
    m = 0
    for road in data.roads:
        roadBackup = road.backupNum()
        if  roadBackup > m:
            m = roadBackup
    return m
    
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
    curMax = curMaxBackup (data) 
    if curMax > data.maxBack:
        data.maxBack = curMax #update the maximum backup 
    if not data.set:
        data.t += 1
        for road in data.roads:
        # timer fires #potentially gotta somehow interleave the road and intersection timers. .... somehow it isn't getting run at the same time.... 
            road.timerFiredRoad(data, time.time())
        for i in data.intersecs:
            data.intersecs[i].timerFiredIntersec (data)
        
        

def redrawAll(canvas, data):
    if not data.error:
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
    else:
        canvas.create_text (data.width//8, data.height//4, text = data.errorMsg, fill = "red", font="Times 20 bold", anchor = "nw")

def setTheLights(data, lights):
    j = 0
    for i in data.intersecs:
        data.intersecs[i].NSTime = lights [j][0]
        data.intersecs[i].EWTime = lights [j][1]
        j += 1
    

####################################
# use the run function as-is from the 112 website
####################################

def run(set, width=300, height=300, lights = None, roads = [], intersecs = {}, error = False, errorMsg = "", slow = False):
    def redrawAllWrapper(canvas, data):
    
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()  
    def inputRate ():
        data.rate= int(inputRate.get())  
    def inputSpeedLim ():
        data.speedLim = int(inputSpeedL.get())  
    def inputWeightBack ():
        data.weightBack = int(inputWeightB.get())  
    def inputWeightAvgWait ():
        data.weightAvgWait = int(inputWeightW.get())  

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
    if not slow: data.timerDelay = 1 # milliseconds
    if slow: data.timerDelay = 20 # wtf this is faster teehee.... try making delay just increase m?
    root = Tk()
    #syntax for the background color from https://stackoverflow.com/questions/2744795/background-color-for-tk-in-python
    #function and button to close window from https://stackoverflow.com/questions/9987624/how-to-close-a-tkinter-window-by-pressing-a-button/9987684
    def close_window (): 
        root.destroy()
        
    root ["bg"] = "black"
    root.resizable(width=False, height=False) # prevents resizing window
    init(data, roads, intersecs, set, error, errorMsg)
    
    #button and text syntax from Edward Lu (elu2) 
    rateFrame = Frame (root, borderwidth = 2, relief = "solid")
    inputRate = Entry (rateFrame, borderwidth = 2, relief = "solid")
    buttonRate = Button (rateFrame, command = inputRate, width = 20, height = 1,
        text = "secs between cars")
    speedFrame = Frame (rateFrame, borderwidth = 2, relief = "solid")
    inputSpeedL = Entry (speedFrame, borderwidth = 2, relief = "solid")
    buttonSpeed = Button (speedFrame, command = inputSpeedLim, width = 20, height = 1,
        text = "speed limit")
    weightBFrame = Frame (rateFrame, borderwidth = 2, relief = "solid")
    inputWeightB= Entry (weightBFrame, borderwidth = 2, relief = "solid")
    buttonWeightB = Button (weightBFrame, command = inputWeightBack, width = 20, height = 1,
        text = "weight # backup")   
    weightWFrame = Frame (rateFrame, borderwidth = 2, relief = "solid")
    inputWeightW = Entry (weightWFrame, borderwidth = 2, relief = "solid")
    buttonWeightW = Button (weightWFrame, command = inputWeightAvgWait, width = 20, height = 1,
        text = "weight avg waitTime") 
    
    
    if data.set:
        text = "done drawing roads"
    else:
        text = "new simulation"
    
    button = Button (rateFrame, text = text, width = 20, command = close_window)
    
    if not data.set:
        setTheLights(data, lights)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    
    canvas.pack(side = RIGHT)
    if data.set:
        rateFrame.pack (side = LEFT, fill = Y)
        inputRate.pack (side = TOP)
        buttonRate.pack (side = TOP)
        speedFrame.pack (side = TOP)
        inputSpeedL.pack (side = TOP)
        buttonSpeed.pack (side = TOP)
        weightBFrame.pack (side = TOP)
        inputWeightB.pack (side = TOP)
        buttonWeightB.pack (side = TOP)
        weightWFrame.pack (side = TOP)
        inputWeightW.pack (side = TOP)
        buttonWeightW.pack (side = TOP)
    
    rateFrame.pack (side = LEFT, fill = Y)
    button.pack (side = LEFT)
    
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
        return (SideIntersection.totalTimeWaiting, SideIntersection.totalCars, avgTimeSpentWaiting(), data.maxBack) 
    else:
        replaceIntersections(data)
        return (data.roads, data.intersecs, data.error, data.errorMsg, data.weightBack, data.weightAvgWait)
    print("bye!")

