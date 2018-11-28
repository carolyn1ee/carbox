from intersections import *
# almost exactly the same as the intersection you are replacing but it kills
# the cars as the go off screen and keeps the light green 
class SideIntersection (Intersection):
    totalTimeWaiting = 0
    totalCars = 0
    def __init__(self, data, intersec):
        x = intersec.x
        y = intersec.y
        roadsNS = intersec.roadsNS
        roadsEW = intersec.roadsEW
        NSTime = intersec.NSTime
        EWTime = intersec.EWTime
        staggerTime = intersec.staggerTime
        super().__init__ (data, x, y, NSTime, EWTime, staggerTime, roadsNS,
                                    roadsEW)
        self.data = data
    def intersecCopy (self, roads):
        return SideIntersection (self.data, super().intersecCopy(roads))
    def pickUpCars (self, data):
        for road in self.roadsNS:
            if road [1] == "P":
                tmpCar = road[0].carOutP(data)
                if tmpCar != None:
                    SideIntersection.totalTimeWaiting += tmpCar.totalTime
                    SideIntersection.totalCars += 1
                    road[0].carsListP.remove (tmpCar)
            elif road [1] == "N":
                tmpCar = road[0].carOutN(data)
                if tmpCar != None:
                    SideIntersection.totalTimeWaiting += tmpCar.totalTime
                    SideIntersection.totalCars += 1
                    road[0].carsListN.remove (tmpCar)
        for road in self.roadsEW:
            if road[1] == "P":
                tmpCar = road[0].carOutP(data)
                if tmpCar != None:
                    SideIntersection.totalTimeWaiting += tmpCar.totalTime
                    SideIntersection.totalCars += 1
                    road[0].carsListP.remove (tmpCar)
            elif road [1] == "N":
                tmpCar = road[0].carOutN(data)
                if tmpCar != None:
                    SideIntersection.totalTimeWaiting += tmpCar.totalTime
                    SideIntersection.totalCars += 1
                    road[0].carsListN.remove (tmpCar)
    # just makes all the lights on the side green so the cars can just flow out
    def checkLights (self, data):
        self.lightNS = 1
        self.lightEW = 1
        for roadList in [self.roadsNS, self.roadsEW]:
            self.changeLights (roadList, 1)
    def drawLightNS (self,data, canvas):
        pass
    def drawLightEW (self, data, canvas):    
        pass
        
