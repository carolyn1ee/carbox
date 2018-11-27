from Simulator import *

import random
roads, intersecs = run(set=True, width=800, height=800, lights = None, roads = [], intersecs = {})


###create times
#can make it better by only setting the lights for the nonside intersections
lights =  [[None, None] for i in range (len (intersecs))]

def createTimes ():
    for i in range(len(intersecs)):
        lights [i][0] = random.choice ([3, 4, 5, 6])
        lights [i][1] = random.choice ([3, 4, 5, 6])
createTimes ()

##run

#look in simulator and see why nothing is drawing like cars or lights
print (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs))
print (9)
print (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs))
#try running and resetting a debugger????
def optimize (runs):
    minAvg = 10**99
    for r in range (runs):
        createTimes()
        print (10)
        tmpAvg = (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs)) [2]
        print (9)
        if minAvg > tmpAvg:
            print (8)
            minAvg = tmpAvg
            minLights = lights
        print (7)
    print (6)
    print ("ok look here are your nice nice lights")
    print (minAvg)
    
#optimize (3)
        