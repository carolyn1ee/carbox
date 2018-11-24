from roads import *
from sideRoads import *
from intersections import *



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

def setInOrder (x, y):
    if x > y:
        tmp = y
        y = x
        x = tmp
#makes it so that the start value is less than the end value
def setTmpsInOrder (data):
    setInOrder (data.tmpStartX, data.tmpEndX)
    setInOrder (data.tmpStartY, data.tmpEndY)

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
    if not (x, y) in data.intersecs:
        intersec = Intersection (data, x=x, y=y)
        data.intersecs [(x,y)] = intersec
    if data.roadDir == [0,1]:
        data.intersecs[(x, y)].roadsNS.append ([road, side])
    elif data.roadDir == [1,0]:
        data.intersecs[(x, y)].roadsEW.append ([road, side])
   
def createRoad (data):
    setTmpsInOrder (data)
    findDir (data)
    if isASideRoad (data):
        #create some kind of input to allow user to set the time between cars
        road = SideRoad (data, dir = data.roadDir, xN = data.tmpStartX,
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY, secsBtCars=3) 
            #if anything goes wrong,
        # it may be bc of ordering of the inputs is messed up and then you have default vals too
    else:
        road = Road (data, dir = data.roadDir, xN = data.tmpStartX,
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY)
    return road
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
    if event.keysym == "space":
        # only starts the cars if we are go
        data.go = True 
    if event.keysym == "Return":
        #now need to create the road
        #make the start and end be in increasing order
        #find the direction
        #see if it is on the edge
        # create a road
        #4)find if there is already an intersection
        #5)create intersection or add to intersection (this is done in the intersection function)
        road = createRoad (data)
        createIntersection (data, data.tmpStartX, data.tmpStartY, "N", road)
        createIntersection (data, data.tmpEndX, data.tmpEndX, "P", road)
        data.roads += [road]
        
## here is a f'n to call
# this draws the road you are considering creating as you move your arrow keys along....
def drawTmp (canvas, data):
    canvas.create_line (data.tmpStartX, data.tmpStartY, data.tmpEndX, 
            data.tmpEndY, fill = "white", width = 3)
            