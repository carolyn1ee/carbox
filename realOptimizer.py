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
    r, i, err, errMsg, weightBackup, weightTime = run(set=True, width=800, height=800, lights = None, roads = [], intersecs = {})
    lights =  [[None, None] for i in range (len (i))]
    minBad = 10**99
    for y in range (runs):
        createTimes(i, lights)
        roads = copyRoads (r)
        intersecs = copyIntersecs (i, roads)
        
        tmpAvg, tmpMaxBack = (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs, error = err, errorMsg = errMsg)) [2:4]
        
        if tmpAvg == None:
            #####
            print ("you need to let the thing run for a little bit so you get a bit of data" + 42/0)
        if minBad > tmpAvg * weightTime +  tmpMaxBack * weightBackup:
            minBad = tmpAvg * weightTime +  tmpMaxBack * weightBackup
            minAvg = tmpAvg
            minBack = tmpMaxBack 
            minLights = lights
    (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs, error = True, errorMsg = "here is the minimum avg time waiting at the lights: "+ str(round (minAvg, 2))+"\nand this is is the maximum number of cars that were backed up \nat an intersection in the best simulation: " + str (minBack) + "\n\n\nHere is the minimum badness level: " + str(round (minBad, 2)) + "=" + str(round(minAvg, 2)) + " * " + str(weightTime) + " + " + str (minBack) + " * " + str (weightBackup) + " \nand this is the best timing \nfor the lights on the next screen."))
    roads = copyRoads (r)
    intersecs = copyIntersecs (i, roads)
    (run (set = False, width = 800, height = 800, lights = minLights, roads = roads, intersecs = intersecs, error = False, errorMsg = "", slow = True))
    
optimize (3)
        