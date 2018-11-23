from simulation import *

        # has a list of the roads that run thru it and can control what cars go thru for each intersection. just makes all the parallel ones go simultaneously. if it is not 4way then teh roads can handle moving the cars right or left. otherwise, the cars are only going to go straight.
        
        # there are only 1 or 2 cars in roadsNS or roads EW....
        
        # needs to handle the cars that are going through the intersection
class Intersection (object):
    def __init__(self, data, roadsNS, roadsEW, x, y, NSTime, EWTime, staggerTime):
        self.roadsNS = roadsNS
        self.roadsEW = roadsEW
        self.NSTime=NSTime
        self.EWTime = EWTime
        self.x = x
        self.y = y
        self.cycleLen = NSTime + EWTime + 2*data.yellowTime
        #sometimes you don't want to start with NS being green. sometimes, want
        #to stagger the times 
        self.staggerTime = staggerTime
    
    def changeLights (roadsList, light):
        for road in roadsList:
            road.Light = light
    
    def checkLights (self, data):
        if timerIsNSecs (data, self.cycle, self.staggerTime):
            changeLights (roadsNS, 1)
            changeLights (roadsEW, 0)
        elif timerIsNSecs (data, self.cycle, self.NSTime + self.staggerTime):
            changeLights (roadsNS, 2)
            changeLights (roadsEW, 0)
        elif timerIsNSecs (data, self.cycle, self.yellowTime + \
                            self.NSTime + self.staggerTime):
            changeLights (roadsNS, 0)
            changeLights (roadsEW, 1)
        elif timerIsNSecs (data, self.cycle, self.EWTime+ self.yellowTime + \
                            self.NSTime + self.staggerTime):
            changeLights (roadsNS, 0)
            changeLights (roadsEW, 2)
            
            
##view
     #draws cars in the intersection   
    def drawIntersecCars ():
        pass