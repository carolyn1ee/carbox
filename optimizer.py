from Simulator import *
import copy
import random
import intersections
import roads
r, i = run(set=True, width=800, height=800, lights = None, roads = [], intersecs = {})
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
roads = copyRoads (r)
intersecs = copyIntersecs (i, roads)
print ("\n\n\nintersections copying result \n" + str(intersecs))

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
# print (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs))
# print (9)
# 
# print (000000)
# roads = copyRoads (r)
# intersecs = copyIntersecs (i, roads)
# print (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs))
def optimize (runs, r, i):
    minAvg = 10**99
    for y in range (runs):
        createTimes()
        roads = copyRoads (r)
        intersecs = copyIntersecs (i, roads)
        tmpAvg = (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs)) [2]
        if tmpAvg == None:
            print ("you need to let the thing run for a little bit so you get a bit of data" + 42/0)
        if minAvg > tmpAvg:
            minAvg = tmpAvg
            minLights = lights
    print ("ok look here are your nice nice lights" + str(minLights))
    print ("here is the minimum avg" + minAvg)
    
optimize (3, r, i)
        