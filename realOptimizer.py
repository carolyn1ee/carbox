 #runs the setup and simulator
from Simulator import *
import copy
import random
import intersections
import roads
def copyRoads (roads):
    l = []
    for r in roads:
        l += [r.roadCopy()]
    return l
def copyIntersecs (intersecs, roads):
    l={}
    for r in intersecs:
        l[r] = intersecs[r].intersecCopy(roads)
    return l

###create times
#can make it better by only setting the lights for the nonside intersections

def createTimes (intersecs, lights):
    for i in range(len(intersecs)):
        lights [i][0] = random.choice ([3, 4, 5, 6])
        lights [i][1] = random.choice ([3, 4, 5, 6])

##run
 
def optimize (runs):
    r, i, err, errMsg = run(set=True, width=800, height=800, lights = None, roads = [], intersecs = {})
    lights =  [[None, None] for i in range (len (i))]
    minAvg = 10**99
    for y in range (runs):
        createTimes(i, lights)
        #print ("ROADS ORIGINAL" + str(r) + "\n\n\n\n")
        print ("INTERSECS ORIGINAL" + str (i) + "\n\n\n\n\n\n\n\n\n\n")
        roads = copyRoads (r)
        intersecs = copyIntersecs (i, roads)
        print ("NEW INTERSECS" + str(intersecs) + "\n\n\n\n\n\n\n\n\n\n")
        
        tmpAvg = (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs, error = err, errorMsg = errMsg)) [2]
        print ("AFTER SIMULATION" + str(intersecs) + "\n\n\n\n\n\n\n\n\n\n")
        
        if tmpAvg == None:
            #####
            print ("you need to let the thing run for a little bit so you get a bit of data" + 42/0)
        if minAvg > tmpAvg:
            minAvg = tmpAvg
            minLights = lights
    (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs, error = True, errorMsg = "here is the minimum avg: "+ str(minAvg)+" and this is the timing \nfor the lights on the next screen."))
    roads = copyRoads (r)
    intersecs = copyIntersecs (i, roads)
    (run (set = False, width = 800, height = 800, lights = minLights, roads = roads, intersecs = intersecs, error = False, errorMsg = "", slow = True))
    
optimize (3)
        