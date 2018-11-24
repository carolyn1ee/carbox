def mousePressedC (event, data):
    data.tmpStartX = event.x
    data.tmpStartY = event.y
    data.tmpEndX = data.tmpStartX
    data.tmpEndY = data.tmpStartY

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
    if data.dir == "Up" or data.dir == "Down":
        data.roadDir = [0,1]
    if data.dir == "Right" or data.dir == "Left":
        data.roadDir = [1,0]

def isASideRoad (data):
    #check if any of the start coordinates is 0 or beyond edge of screen
    return data.tmpStartX *data.tmpStartY <= 0 or data.tmpEndX >= data.width or\
        data.tmpEndY >= data.height

def createRoad (data):
    if isASideRoad (data):
        #create some kind of input to allow user to set the time between cars
        road = SideRoad (data, dir = data.roadDir, xN = data.tmpStartX,
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY, secsBtCars=3) 
            #if anything goes wrong,
        # it may be bc of ordering of the inputs is messed up and then you have default vals too
    else:
        road = Road (data, dir = data.roadDir, xN = data.tmpStartX,
            yN = data.tmpStartY, xP = data.tmpEndX, yP = data.tmpEndY)
    data.roads += [road]

def keyPressedC (event, data):
    if event.keysym == "Up":
        if data.tmpDir != "Up":
            #need to update dir and then need to restart the tmp
            data.tmpDir = "Up"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndY += data.increment
    if event.keysym == "Down":
        if data.tmpDir != "Down":
            data.tmpDir = "Down"
            data.tmpEndX = data.tmpStartX
            data.tmpEndY = data.tmpStartY
        data.tmpEndY -= data.increment
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
        #5)create intersection or add to intersection
        createARoad (data)
        pass
def drawTmp (canvas, data):
    canvas.create_line (data.tmpStartX, data.tmpStartY, data.tmpEndX, 
            data.tmpEndY, fill = "white", width = 3)
            