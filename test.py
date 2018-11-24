# Updated Animation Starter Code


from tkinter import *
from PIL import ImageTk,Image  
from roads import *
from sideRoads import *
from intersections import *
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.NSTime = 5
    data.EWTime = 5
    data.yellowTime = 1
    #interval of seconds between each car that enters
    data.EWCarRate = 5
    data.NSCarRate = 2
    data.WECarRate = 3
    data.SNCarRate = 4
    data.roads = []
    data.sideRoads = []
    # adding hardcoded roads: need to have side roads that add cars

     
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
    # load data.xyz as appropriate
    
    data.intersecRad = 40
    data.road = SideRoad (data, dir = [0,1], xN = data.width//2,\
        yN = data.height//2, xP = data.width//2, yP = data.height, 
        carsListP = [], carsListN = [], speedLimit = 10, secsBtCars = 2)
    data.road2 = SideRoad (data, dir = [0,1], xN = data.width//2,\
        yN = 0, xP = data.width//2, yP = data.height//2, 
        carsListP = [], carsListN = [], speedLimit = 10, secsBtCars = 4)
    data.road3 = SideRoad (data, dir = [1,0], xN = 0,\
        yN = data.height//2, xP = data.width//2, yP = data.height//2, 
        carsListP = [], carsListN = [], speedLimit = 10, secsBtCars = 5)
    data.road4 = SideRoad (data, dir = [1,0], xN =data.width//2,\
        yN = data.height//2, xP = data.width, yP = data.height//2, 
        carsListP = [], carsListN = [], speedLimit = 10, secsBtCars = 7)
    data.intersection = Intersection(data, roadsNS = [[data.road , "N"], [data.road2, "P"]], roadsEW = [[data.road3, "P"], [data.road4, "N"]], x = data.width//2, y = data.height // 2, NSTime = 3, EWTime = 2, staggerTime = 1)

    
def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def timerFired(data):
    data.t += 1
    
    for road in [data.road, data.road2, data.road3, data.road4]:
        road.timerFiredRoad(data)
    data.intersection.timerFiredIntersec (data)

def redrawAll(canvas, data):
    canvas.create_rectangle (data.width//2 - data.intersecRad, data.height//2 - data.intersecRad, data.width//2 + data.intersecRad, data.height//2 + data.intersecRad, fill = "white")
    #for i in range (data.width//10):
        #canvas.create_line()
    canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
    #canvas.create_rectangle (data.road.xF, data.road.yF, data.road.xF +10, data.road.yF +10, fill = "white")
    for road in [data.road, data.road2, data.road3, data.road4]:
        road.drawAllRoad(canvas, data)
    data.intersection.drawIntersecCars(canvas)

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











################################################


##########3
###########
#########
################################################# Basic Animation Framework ur bad
