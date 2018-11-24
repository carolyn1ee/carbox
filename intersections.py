#from simulation import *
from roads import *
        # has a list of the roads that run thru it and can control what cars go thru for each intersection. just makes all the parallel ones go simultaneously. if it is not 4way then teh roads can handle moving the cars right or left. otherwise, the cars are only going to go straight.
        
        # there are only 1 or 2 roads in roadsNS or roads EW....
        
        # needs to handle the cars that are going through the intersection: picks them up as they enter intersection and then drops them off as they go into next road.
class Intersection (Road):
    def __init__(self, data, roadsNS, roadsEW, x, y, NSTime, EWTime, staggerTime):
        self.roadsNS = roadsNS
        self.roadsEW = roadsEW
        self.NSTime=NSTime
        self.EWTime = EWTime
        self.x = x
        self.y = y
        self.cycle = NSTime + EWTime + 2*data.yellowTime
        #sometimes you don't want to start with NS being green. sometimes, want
        #to stagger the times 
        self.staggerTime = staggerTime
        self.carsEW = []
        self.carsWE = []
        self.carsNS = []
        self.carsSN = []
    
    def changeLights (self, roadsList, light):
        for road in roadsList:
            #need to check which side of the road is in this intersection
            if road[1] == "P":
                road[0].lightP = light
            elif road [1] == "N":
                road[0].lightN = light
    
    def checkLights (self, data):
        if self.timerIsNSecs (data, self.cycle, self.staggerTime):
            self.changeLights (self.roadsNS, 1)
            self.changeLights (self.roadsEW, 0)
            print ("NS")
        elif self.timerIsNSecs (data, self.cycle, self.NSTime + self.staggerTime):
            self.changeLights (self.roadsNS, 2)
            self.changeLights (self.roadsEW, 0)
        elif self.timerIsNSecs (data, self.cycle, data.yellowTime + \
                            self.NSTime + self.staggerTime):
            self.changeLights (self.roadsNS, 0)
            self.changeLights (self.roadsEW, 1)
            print ("EW")
        elif self.timerIsNSecs (data, self.cycle, self.EWTime + data.yellowTime + \
                            self.NSTime + self.staggerTime):
            self.changeLights (self.roadsNS, 0)
            self.changeLights (self.roadsEW, 2)
    #handle cars coming thru the intersection:
        #takes cars that are coming into the intersection so that it can deal w/
    def pickUpCars (self, data):
        for road in self.roadsNS:
            if road [1] == "P":
                if road[0].lightP == 1:
                    tmpCar = road[0].carOutP(data)
                    if tmpCar != None:
                        self.carsNS += [tmpCar]
                        road[0].carsListP.remove (tmpCar)
            elif road [1] == "N":
                if road[0].lightN == 1:
                    tmpCar = road[0].carOutN(data)
                    if tmpCar != None:
                        self.carsSN += [tmpCar]
                        road[0].carsListN.remove (tmpCar)
        for road in self.roadsEW:
            if road [1] == "P":
                if road[0].lightP == 1:
                    tmpCar = road[0].carOutP(data)
                    if tmpCar != None:
                        self.carsWE += [tmpCar]
                        road[0].carsListP.remove (tmpCar)
            elif road [1] == "N":
                if road[0].lightN == 1:
                    tmpCar = road[0].carOutN(data)
                    if tmpCar != None:
                        self.carsEW += [tmpCar]
                        road[0].carsListN.remove (tmpCar)
    def dropOffCars (self, data):
        for road in self.roadsNS:
            if road[1] =="N":
                for car in self.carsNS:
                    #if out of intersection, get rid of this car and create a new car 
                    #to stick in the other road
                    if car.y >= data.intersecRad + self.y:
                        road[0].carsListP.append (car)
                        road[0].carsListP[-1].speedMax = road[0].speedLimit
                        self.carsNS.remove(car)
            #going up : drop off in P
            if road [1] == "P":
                for car in self.carsSN:
                    if car.y <= -data.intersecRad + self.y:
                        road[0].carsListN.append (car)
                        road[0].carsListN[-1].speedMax = road[0].speedLimit
                        self.carsSN.remove(car)
        for road in self.roadsEW:
            if road[1] =="N":
                for car in self.carsWE:
                    if car.x >= data.intersecRad + self.x:
                        road[0].carsListP.append (car)
                        road[0].carsListP[-1].speedMax = road[0].speedLimit                                                        
                        self.carsWE.remove(car)
            if road [1] == "P":
                for car in self.carsEW:
                    if car.x <= -data.intersecRad + self.x:
                        road[0].carsListN.append (car)
                        road[0].carsListN[-1].speedMax = road[0].speedLimit
                        self.carsEW.remove(car)
                
    def moveCars (self):
        for carsList in [self.carsEW, self.carsNS, self.carsSN, self.carsWE]:
            for car in carsList:
                car.move()
            
    
    def changeAccelCarsH (self, carsList):
        for c in range(1, len(carsList)):
            car1 = carsList [c]
            car2 = carsList [c-1]
            if car1.isTooClose (car2):
                car1.deceler()
            else:
                car1.acceler()
        if carsList != []:
            carsList[0].acceler()
    def changeAccelAllCars (self):
        self.changeAccelCarsH (self.carsEW)
        self.changeAccelCarsH (self.carsWE)
        self.changeAccelCarsH (self.carsNS)
        self.changeAccelCarsH (self.carsSN)
    
            
    def timerFiredIntersec (self, data):
        self.pickUpCars (data)
        self.dropOffCars(data)
        self.moveCars()
        self.changeAccelAllCars()
        self.checkLights(data)
        #snag cars coming into intersec
        #have some way to draw the cars... pretty similar to the road:
            #1) move cars
            #2) accelerate cars
            #3) once cars get out of intersection, send them to next intersection
            
            
##view
     #draws cars in the intersection   
    def drawIntersecCars (self, canvas):
        for carsList in [self.carsNS, self.carsSN, self.carsEW, self.carsWE]:
            for car in carsList:
                car.draw(canvas)
          ###  #etc#######