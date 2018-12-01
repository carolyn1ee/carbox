# if we are in the set mode, then there will be this instruction and then it will go on to the actual set up.

def redrawAllStart (canvas, data):
    canvas.create_text (data.width//16, data.height//4, text = "Here is a car simulator. \nTo create roads, click where you want the road to start \nand then use the arrow buttons to grow the road. \nA guide line will show you where your road will appear.\nOnce you are happy with where your road is, press enter.\nRoads must end in intersections or off screen.\nWhen putting in a road that comes from offscreen, \nfirst input the rate that you want the cars to come in from that road before drawing it.\nThen press the button to continue on to the simulation.\nPlease allow a moment between each simulation before pressing the button.\n\nPress space to continue.",  fill="white", font="Times 20 bold", anchor = "nw")
    
def keyPressedStart(event, data):
    if event.keysym == "space":
        data.screen = "setScreen"