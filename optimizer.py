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
###################################roads list is a copy and the intersection also has roads, but they aren't the same roads list -- here we WANT some kind of same road list in the intersection as in the roads -- mebbe make a copy of roads and then create intersections around them????? USE HASHING to find out if they are the same
##run

#look in simulator and see why nothing is drawing like cars or lights
print (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs))
print (9)

print (000000)
print (run (set = False, width = 800, height = 800, lights = lights, roads = copyRoads (r), intersecs = copyIntersecs (i, roads)))
# def optimize (runs):
#     minAvg = 10**99
#     for r in range (runs):
#         createTimes()
#         print (10)
#         tmpAvg = (run (set = False, width = 800, height = 800, lights = lights, roads = roads, intersecs = intersecs)) [2]
#         print (9)
#         if minAvg > tmpAvg:
#             print (8)
#             minAvg = tmpAvg
#             minLights = lights
#         print (7)
#     print (6)
#     print ("ok look here are your nice nice lights")
#     print (minAvg)
#     
#optimize (3)
        