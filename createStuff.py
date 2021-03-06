#handles the user input to create new roads and intersections where user wants them
#event based tkinter from course website
from roads import *
from sideRoads import *
from intersections import *
from sideIntersections import *
from threeWayIntersec import *

#has functions for all the things necessary to create your custom roads. so far we don't have intersections that can handle only 3 roads so that's lame but this file should allow you to 
#click and begin a road
#use arrow keys to start to try to make a road in a direction that you like-- restarts if you try to go in another direction but with same click start. you can only go vert or hor so that's lame too
# when you press the enter key, it will create the road where you wanted it to be.
### pls make some checks so that you can see if there are at least three roads per intersectioni don't have any checks in place so you better create legit roads or it will break
#when you press the space key the cars will start to flow out


#snaps to the grid of increments when creating roads (this way there are fewer
# places to draw roads and we can actually hook up the 
#intersections bc you won't miss it)
def roundToIncrement(data, n):
    if n%data.increment>=data.increment/2:
        return n//data.increment * data.increment + data.increment
    else:
        return n//data.increment * data.increment

##here is a f'n to call
def mousePressedC (event, data):
    data.tmpStartX = roundToIncrement (data, event.x)
    data.tmpStartY = roundToIncrement (data, event.y)
    data.tmpEndX = data.tmpStartX
    data.tmpEndY = data.tmpStartY
    data.tmpDir = None

def setBounds(data):
    #start a bit off screen so that your cars don't pile up
    if data.tmpStartX < 0: data.tmpStartX = (0 - 100)
    if data.tmpStartY < 0: data.tmpStartY = (0 - 100)
    if data.tmpEndX > data.width: data.tmpEndX = (data.width + 100)
    if data.tmpEndY > data.height: data.tmpEndY = (data.height + 100)


# functions for when you want to create a road
#makes it so that the start value is less than the end value
def setTmpsInOrder (data):
    if data.tmpStartX > data.tmpEndX:
        tmp = data.tmpEndX
        data.tmpEndX = data.tmpStartX
        data.tmpStartX = tmp
    if data.tmpStartY > data.tmpEndY:
        tmp = data.tmpEndY
        data.tmpEndY = data.tmpStartY
        data.tmpStartY = tmp

def findDir (data):
    if data.tmpDir == "Up" or data.tmpDir == "Down":
        data.roadDir = [0,1]
    if data.tmpDir == "Right" or data.tmpDir == "Left":
        data.roadDir = [1,0]

def isASideRoad (data):
    #check if any of the start coordinates is 0 or beyond edge of screen
    return data.tmpStartX *data.tmpStartY <= 0 or data.tmpEndX >= data.width or\
        data.tmpEndY >= data.height

#adds the road to an existing intersection if it exists, otherwise creates an
# intersection and puts the road into it.
#side is  "N" or "P" depending on which side you are sticking in an intersection
def createIntersection(data, x, y, side, road):
    intLoc = (x,y)
    if not (intLoc in data.intersecs):
        intersec = Intersection (data, x=x, y=y)
        data.intersecs [intLoc] = intersec
    if data.roadDir == [0,1]:
        data.intersecs[intLoc].roadsNS = data.intersecs[intLoc].roadsNS + [[road, side]]
    elif data.roadDir == [1,0]:
        data.intersecs[intLoc].roadsEW =  data.intersecs[intLoc].roadsEW + [[road, side]]
   
def createRoad (data):
    setTmpsInOrder (data)
    setBounds (data)
    findDir (data)
    if isASideRoad (data):
        road = SideRoad (data, dir = data.roadDir, xN = data.tmpStartX,\
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY, secsBtCars = int(data.rate), speedLimit = int(data.speedLim))
            
            
    else:
        road = Road (data, dir = data.roadDir, xN = data.tmpStartX,
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY, speedLimit = int(data.speedLim))
    return road

#makes sure the intersections are the right type once you are done drawing them 
#the intersections on the end should be replaced with intersections for the end
def replaceIntersections (data):
    for i in data.intersecs:
        if data.intersecs[i].countNumRoads () == 1:
            endIntersec = SideIntersection (data, data.intersecs[i])
            data.intersecs[i] = endIntersec 
        elif data.intersecs[i].countNumRoads () == 3:
            threeInt = ThreeWyIntersec (data, data.intersecs[i])
            data.intersecs [i] = threeInt
        elif data.intersecs [i].countNumRoads() == 2:
            data.errorMsg = "Please draw roads so that every intersection has a 4-way or 3-way"
            data.error = True
## here is a f'n to call
def keyPressedC (event, data):
    if event.keysym == "Up":
        if data.tmpDir != "Up":
            #need to update dir and then need to restart the tmp
            data.tmpDir = "Up"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndY -= data.increment
    if event.keysym == "Down":
        if data.tmpDir != "Down":
            data.tmpDir = "Down"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndY += data.increment
    if event.keysym == "Left":
        if data.tmpDir != "Left":
            data.tmpDir = "Left"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndX -= data.increment
    if event.keysym == "Right":
        if data.tmpDir != "Right":
            data.tmpDir = "Right"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndX += data.increment
    # if event.keysym == "space":
    # #     only starts the cars if we are  go
    #     data.go = True 
    #     replaceIntersections (data)
        

    if event.keysym == "Return":
        #now need to create the road
        #make the start and end be in increasing order
        #find the direction
        #see if it is on the edge
        # create a road
        #4)find if there is already an intersection
        #5)create intersection or add to intersection (this is done in the intersection function)
        # need to make sure that the road isn't trivial
       # if data.tmpStartX - data.tmpEndX == data.tmpStartY - data.tmpEndY:
       #make sure that your roads aren't too short
        if abs (data.tmpEndX - data.tmpStartX) > 150 or abs (data.tmpEndY - data.tmpStartY) > 150:
            road = createRoad (data)
            createIntersection (data, data.tmpStartX, data.tmpStartY, "N", road)
            createIntersection (data, data.tmpEndX, data.tmpEndY, "P", road)
            data.roads += [road]
            data.tmpStartX = data.tmpEndX
            data.tmpStartY = data.tmpEndY

## here is a f'n to call
# this draws the road you are considering creating as you move your arrow keys along....
def drawTmp (canvas, data):
    canvas.create_line (data.tmpStartX, data.tmpStartY, data.tmpEndX, 
            data.tmpEndY, fill = "white", width = 3)
            