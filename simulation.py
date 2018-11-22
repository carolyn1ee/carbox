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
    #UI will set this but here are some default vals
    #amt of time in secs for the light to be green
    data.NSTime = 5
    data.EWTime = 5
    data.yellowTime = 1
    #interval of seconds between each car that enters
    data.EWCarRate = 5
    data.NSCarRate = 2
    data.WECarRate = 3
    data.SNCarRate = 4


     
    #set car lists
    data.carsSN = []
    data.carsWE = []
    data.carsNS = []
    data.carsEW = []
    data.allCars = [data.carsSN, data.carsNS, data.carsEW, data.carsWE]
    #intersection:
    #green light means 1 and red light means 0
    data.NS = 1
    data.EW = 0
    data.t = 0
    
    data.yellowLightImg = PhotoImage(file="imgs/yellowLight.gif")
    data.redLightImg = PhotoImage(file="imgs/redLight.gif")
    data.greenLightImg = PhotoImage(file="imgs/greenLight.gif")

    
    data.radius = 20
    data.intersecRad = 40
    #center of the intersection
    data.intersecX = data.width//2
    data.intersecY = data.height//2
    
    data.firstCarEW = None
    data.firstCarWE = None
    data.firstCarNS = None
    data.firstCarSN = None

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass
    
    
    
    
    ######
####TIMER
    ######
    
##helper f'ns
#returns true every m seconds (m is for mod), staggaring at n
def timerIsNSecs (data, m, n=0):
    #timerFired goes off 10 times per sec
    firesPerSec = 10 
    return data.t % (firesPerSec * m) == n*firesPerSec

#returns if the car is in intersection
# def inIntersection (data, car):
#     return car.x < data.intersecX + data.intersecRad and car.x > data.intersecX - data.intersecRad and car.y < data.intersecY + data.intersecRad and car.y > data.intersecY - data.intersecRad 

#tells you if a given car is in past the area where the car 
#needs to slow down in order to not fall into the intersection.
def inSlowArea (data, car, dir):
    if car == None:
        return False
    if dir == "NS":
        return car.y >= data.intersecY -data.intersecRad - car.buffer()
    if dir == "SN":
        return car.y <= data.intersecY + data.intersecRad + car.buffer()
    if dir == "EW":
        return car.x <= data.intersecX + data.intersecRad + car.buffer()
    if dir == "WE":
        return car.x >= data.intersecX - data.intersecRad - car.buffer()



#given direction ("NS" etc) returns the first car object that is in front of the
# intersection and in front enough that it can stop before intersection
def frontOfQueue (data, carList, dir):
    if dir == "NS":
        for car in carList:    
            if car.y < data.intersecY - data.intersecRad - car.buffer():
                return car
    elif dir == "SN":
        for car in carList:
            if car.y > data.intersecY + data.intersecRad + car.buffer():
                return car
    elif dir == "EW":
        for car in carList:
            if car.x > data.intersecX + data.intersecRad + car.buffer():
                return car
    elif dir == "WE":
        for car in carList:
            if car.x < data.intersecX - data.intersecRad - car.buffer():
                return car
                
def moveCarsInList (l):
    for car in l:
        car.move()
        

            
def changeLights(data):
    #cycle is the amt of time for the lights to go thru a complete cycle
    data.cycle = data.NSTime + data.EWTime + 2*data.yellowTime
    if timerIsNSecs (data, data.cycle):
        data.NS = 1
        data.EW = 0
    elif timerIsNSecs (data, data.cycle, data.NSTime):
        data.NS = 2
        data.EW = 0
    elif timerIsNSecs (data, data.cycle, data.yellowTime + \
                        data.NSTime):
        data.NS = 0
        data.EW = 1
    elif timerIsNSecs (data, data.cycle, data.EWTime+ data.yellowTime + \
                        data.NSTime):
        data.NS = 0
        data.EW = 2

#gets rid of the cars that go off screen
def killCarsOffScreen (data):
    for carList in data.allCars:
        for car in carList:
            if car.x >data.width or car.x<0 or car.y>data.height or car.y<0:
                carList.remove(car)
    
##actual timer

def timerFired(data):
    killCarsOffScreen(data)
    data.t += 1
    firesPerSec = 10 
#will change the hardcoded values later to be in some random range for the 
#acceleration and the speed when creating new car objects
#adding cars 
    if timerIsNSecs (data, data.NSCarRate):
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
#moving cars
    for l in data.allCars:
        moveCarsInList(l)
        
    
    
    #slow down the cars for when they get too close to the car in front
    #but speed them up if they have space but only speed up if they aren't the 
    #first car in the intersection
    for carList in [data.carsWE, data.carsEW,
    data.carsNS, data.carsSN]:
        for c in range(1, len(carList)):
            if carList[c].isTooClose(carList[c-1]):
                carList[c].deceler()
            elif carList [c] != data.firstCarNS and \
            carList [c] != data.firstCarSN and \
            carList [c] != data.firstCarEW and\
            carList [c] != data.firstCarWE:
                carList[c].acceler() 
        if carList != [] and carList [0] != data.firstCarNS and \
            carList [0] != data.firstCarSN and \
            carList [0] != data.firstCarEW and\
            carList [0] != data.firstCarWE:
            carList[0].acceler()
                #even if the car is first at red light the
                # speed will increase but, 
                #the speed will be reset to 0 in the next lines

    #make the 1st car at the intersection notice yellow so that it will slow
    #when it gets too close
    if (data.NS == 2 or data.NS == 0):
        #need to check if you have already set the first car
        if data.firstCarNS == None:
            data.firstCarNS = frontOfQueue(data, data.carsNS, "NS")
        if data.firstCarSN == None: 
            data.firstCarSN = frontOfQueue(data, data.carsSN, "SN")
    else: #if green light, set first car to none to show there is no car 
    #about to go into a red light intersection
        data.firstCarSN = None
        data.firstCarNS = None
        # frontOfQueue(data, data.carsNS, "NS").intersecSlow = True
        # frontOfQueue(data, data.carsSN, "SN").intersecSlow = True
    if (data.EW == 2 or data.EW == 0):
        if data.firstCarEW == None:
            data.firstCarEW = frontOfQueue(data, data.carsEW, "EW")
        if data.firstCarWE == None:
            data.firstCarWE = frontOfQueue(data, data.carsWE, "WE")
    else:
        data.firstCarEW = None
        data.firstCarWE = None
    
    #if yellow or red light, slow down the first car before intersection
    if data.NS == 0 or data.NS == 2:
        if inSlowArea(data, data.firstCarNS, "NS"):
            data.firstCarNS.deceler()
        if inSlowArea (data, data.firstCarSN, "SN"):
            data.firstCarSN.deceler()
    if data.EW == 0 or data.EW == 2:
        if inSlowArea(data, data.firstCarEW, "EW"):
            data.firstCarEW.deceler()
        if inSlowArea(data, data.firstCarWE, "WE"):
            data.firstCarWE.deceler()
   
    changeLights (data)
                
    ####
## view
    ####

def drawCarsInList (canvas, data, l):
    #from course website: image syntax
    for car in l:
        car.draw(canvas)


        
def stopLightColor (light):
    if light == 1:
        return 'green'
    elif light == 0: 
        return 'red'
    else:
        return 'yellow'
def stopLightImg (data, light):
    if light == 1:
        return data.greenLightImg
    elif light == 0: 
        return data.redLightImg
    else:
        return data.yellowLightImg
        
def redrawAll(canvas, data):
    drawCarsInList (canvas, data, data.carsNS)
    drawCarsInList (canvas, data, data.carsSN)
    drawCarsInList (canvas, data, data.carsEW)
    drawCarsInList (canvas, data, data.carsWE)

    roadWidth = 100
    stopLightR = 60
    canvas.create_image (data.width // 2 - stopLightR, \
            data.height // 2- roadWidth - stopLightR, \
            image=stopLightImg(data, data.NS) )

    
    canvas.create_image (data.width // 2 - roadWidth - stopLightR, \
            data.height // 2 - stopLightR, \
            image=stopLightImg(data, data.EW) )
   

####################################
# use the run function as-is
#cite: from course website
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    
    def inputNSRate ():
        data.NSCarRate= int(inputNS.get())
    def inputSNRate ():
        data.SNCarRate = int(inputSN.get())
    def inputWERate ():
        data.WECarRate= int(inputWE.get())
    def inputEWRate ():
        data.EWCarRate= int (inputEW.get())
    def inputNSTime ():
        data.NSTime = int (inputNSLight.get())    
    def inputEWTime ():
        data.EWTime = int (inputEWLight.get())

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
    
    #elu2 gave code to do the buttons and input
    leftFrame = Frame (root, borderwidth = 2, relief = "solid")
    
    carRateFrame = Frame (leftFrame, borderwidth = 2, relief = "solid")
    NSFrame = Frame (carRateFrame, borderwidth = 2, relief = "solid")
    inputNS = Entry (NSFrame, borderwidth = 2, relief = "solid")
    buttonNS = Button (NSFrame, command = inputNSRate, width = 20, height = 1,
        text = "NS rate: secs between cars")
    SNFrame = Frame (carRateFrame, borderwidth = 2, relief = "solid")
    inputSN = Entry (SNFrame, borderwidth = 2, relief = "solid")
    buttonSN = Button (SNFrame, command = inputSNRate, width = 20, 
            height = 1, text = "SN rate: secs between cars")
    EWFrame = Frame (carRateFrame, borderwidth = 2, relief = "solid")
    inputEW = Entry (EWFrame, borderwidth = 2, relief = "solid")
    buttonEW = Button (EWFrame, command = inputEWRate, width = 20, height = 1,
        text = "EW rate: secs between cars")
    WEFrame = Frame (carRateFrame, borderwidth = 2, relief = "solid")
    inputWE = Entry (WEFrame, borderwidth = 2, relief = "solid")
    buttonWE = Button (WEFrame, command = inputWERate, width = 20, 
            height = 1, text = "WE rate: secs between cars")
    
    lightsRateFrame =  Frame (leftFrame, borderwidth = 2, relief = "solid")
    NSLight = Frame (lightsRateFrame, borderwidth = 2, relief = "solid")
    inputNSLight = Entry (NSLight, borderwidth = 2, relief = "solid")
    buttonNSLight = Button (NSLight, command = inputNSTime, width = 20, height = 1,
        text = "Time for NS to be green")
    EWLight = Frame (lightsRateFrame, borderwidth = 2, relief = "solid")
    inputEWLight = Entry (EWLight, borderwidth = 2, relief = "solid")
    buttonEWLight = Button (EWLight, command = inputEWTime, width = 20, height = 1,
        text = "Time for EW to be green")
    
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack(side = RIGHT)
    
    #pack the objects nicely on the screen
    leftFrame.pack (side = LEFT, fill = BOTH)
    
    carRateFrame.pack(side = TOP, padx = (1,1), pady = (3,3))
    NSFrame.pack (side = TOP)
    inputNS.pack(side = TOP)
    buttonNS.pack (side = TOP)
    SNFrame.pack (side = TOP)
    inputSN.pack(side = TOP)
    buttonSN.pack (side = TOP)    
    EWFrame.pack (side = TOP)
    inputEW.pack(side = TOP)
    buttonEW.pack (side = TOP)
    WEFrame.pack (side = TOP)
    inputWE.pack(side = TOP)
    buttonWE.pack (side = TOP)
    
    lightsRateFrame.pack (side = TOP, padx = (1,1), pady = (3,1))
    NSLight.pack (side = TOP) 
    inputNSLight.pack (side = TOP)
    buttonNSLight.pack (side = TOP)
    EWLight.pack  (side = TOP)
    inputEWLight.pack (side = TOP)
    buttonEWLight.pack (side = TOP)
    
    
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
