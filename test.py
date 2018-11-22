# Basic Animation Framework

from tkinter import *
from PIL import ImageTk,Image  
from roads import *
# root = Tk()  
# canvas = Canvas(root, width = 300, height = 300)  
#   
# root.mainloop()  
####################################
# customize these functions
####################################

def init(data):
    # load data.xyz as appropriate
    data.intersecRad = 5 
    data.road = Road (data, [0,1], 30, 10, 30, 90, [], [],\
                    [])

def mousePressed(event, data):
    # use event.x and event.y
    pass

def keyPressed(event, data):
    # use event.char and event.keysym
    pass

def redrawAll(canvas, data):
    # canvas.pack()  
    canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
    canvas.create_rectangle (data.road.xF, data.road.yF, data.road.xF +10, data.road.yF +10, fill = "white")
    data.road.drawRoad(canvas, data)

####################################
# use the run function as-is
####################################

def run(width=300, height=300):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='black', width=0)
        redrawAll(canvas, data)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    # Set up data and call init
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
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
    redrawAll(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(400, 200)