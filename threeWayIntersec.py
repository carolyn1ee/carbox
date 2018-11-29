#acts same as intersection but when it has cars, if there is no destination road, 
#it sends the cars to one of the other roads. 
from intersections import *
import random
class ThreeWyIntersec (Intersection):
    def __init__(self, data, intersec):
        x = intersec.x
        y = intersec.y
        NSTime = intersec.NSTime
        EWTime = intersec.EWTime
        staggerTime = intersec.staggerTime
        roadsNS = intersec.roadsNS
        roadsEW = intersec.roadsEW
        super().__init__ (data, x, y, NSTime, EWTime, staggerTime, roadsNS,
                                    roadsEW)
        self.data = data

        if len(self.roadsNS) == 1:
            #remember that lonelyRoad is a list [road, pos or neg]
            self.lonelyRoad = roadsNS[0]
            duoRoads = self.roadsEW
        if len(self.roadsEW) == 1:
            self.lonelyRoad = roadsEW[0]
            #duoRoads is the list of roads that have a road that is straight
            #across.
            duoRoads = self.roadsNS
            
    def intersecCopy (self, roads):
        return ThreeWyIntersec (self.data, super().intersecCopy(roads))
    def __repr__ (self):
        return "threeWay " + super().__repr__()
        
    def pickUpCars (self, data):
        super().pickUpCars (data)
        #mebbe messed up bc tmpCar not defined -- make tmpCar into a data
        if data.tmpCar != None:
            #if i picked up a car, make it decide which way it wants to turn 
            data.tmpCar.t = random.randint (0, 1)
    
    def convertCar (self, car, dir):
        car.dir = dir
        if dir == [0,1]:
            imgFil = Car.carImgNS
        if dir == [0,-1]:
            imgFil = Car.carImgSN
        if dir == [1,0]:
            imgFil = Car.carImgWE
        if dir == [-1, 0]:
            imgFil = Car.carImgEW
        car.img = PhotoImage(file=imgFil)
        
    def dropOffCars (self, data):
        for road in self.roadsNS:
            if not road is self.lonelyRoad:
                if road[1] =="N":
                    for car in self.carsNS:
                        #if out of intersection, get rid of this car and  
                        #stick it in the other road
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
            elif road is self.lonelyRoad:
                if road[1] == "N":
                    #go up and drop off the car upwards. only the first car in this list would be far enough up to go out onto the next road
                    # 0 corresponds to going to the left 
                    ###if self.carsSN != []:
                    for car in self.carsSN:
                        turningCar = car
                        if turningCar.t == 0:
                            if turningCar.y <= self.y - Car.width//2:
                                self.convertCar (turningCar, [-1,0])
                                for road in self.roadsEW:
                                    #need to find the road whose side is providing the left turn
                                    if road[1] == "P":
                                        road[0].carsListN += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsSN.remove(turningCar)
                        elif turningCar.t == 1:
                            if turningCar.y <= self.y + Car.width//2:
                                self.convertCar (turningCar, [1,0])
                                for road in self.roadsEW:
                                    #need to find the road whose side is providing the right turn
                                    if road[1] == "N":
                                        road[0].carsListP += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsSN.remove(turningCar)
                elif road[1] == "P":
                    #then the cars are going down so need to drop them off down
                    ###if self.carsNS != []:
                    for car in self.carsNS:
                        turningCar = car
                        if turningCar.t == 0:
                            if turningCar.y >= self.y - Car.width//2:
                                self.convertCar (turningCar, [-1,0])
                                for road in self.roadsEW:
                                    #need to find the road whose side is providing the left turn
                                    if road[1] == "P":
                                        road[0].carsListN += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsNS.remove(turningCar)
                        elif turningCar.t == 1:
                            if turningCar.y >= self.y + Car.width//2:
                                self.convertCar (turningCar, [1,0])
                                for road in self.roadsEW:
                                    #need to find the road whose side is providing the right turn
                                    if road[1] == "N":
                                        road[0].carsListP += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsNS.remove(turningCar)
                        
        for road in self.roadsEW:
            if not road is self.lonelyRoad:
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
            elif road is self.lonelyRoad:
                if road[1] == "N":
                    #going left
                    # 0 corresponds to going to the up
                    
                    ###if self.carsEW != []:
                    for car in self.carsEW:
                        turningCar = car
                        if turningCar.t == 0:
                            if turningCar.x <= self.x + Car.width//2:
                                self.convertCar (turningCar, [0,-1])
                                for road in self.roadsNS:
                                    #need to find the road whose side is providing the up turn
                                    if road[1] == "P":
                                        road[0].carsListN += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsEW.remove(turningCar)
                        elif turningCar.t == 1:
                            if turningCar.x <= self.x - Car.width//2:
                                self.convertCar (turningCar, [0,1])
                                for road in self.roadsNS:
                                    #need to find the road whose side is providing the right turn
                                    if road[1] == "N":
                                        road[0].carsListP += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsEW.remove(turningCar)
                elif road[1] == "P":
                    #then the cars are going down so need to drop them off down
                    ## if self.carsWE != []:
                    for car in self.carsWE:
                        turningCar = car
                        if turningCar.t == 0:
                            if turningCar.x >= self.x + Car.width//2:
                                self.convertCar (turningCar, [0,-1])
                                for road in self.roadsNS:
                                    #need to find the road whose side is providing the left turn
                                    if road[1] == "P":
                                        road[0].carsListN += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsWE.remove(turningCar)
                        elif turningCar.t == 1:
                            if turningCar.x >= self.x - Car.width//2:
                                self.convertCar (turningCar, [0,1])
                                for road in self.roadsNS:
                                    #need to find the road whose side is providing the right turn
                                    if road[1] == "N":
                                        road[0].carsListP += [turningCar]
                                        turningCar.speedMax = road[0].speedLimit
                                        self.carsWE.remove(turningCar)
                
    def drawAllIntersec (self, data, canvas):
        super().drawAllIntersec(data, canvas)
        if self.lonelyRoad[0].dir == [1,0] and self.lonelyRoad[1] == "N":
            xStart = self.x - data.intersecRad//2
            yStart = self.y + data.intersecRad//2
            xEnd = xStart
            yEnd =  yStart - data.intersecRad
        elif self.lonelyRoad[0].dir == [1,0] and self.lonelyRoad[1] == "P":
            xStart = self.x + data.intersecRad//2
            yStart = self.y - data.intersecRad//2
            xEnd = xStart
            yEnd =  yStart + data.intersecRad
        elif self.lonelyRoad[0].dir == [0,1] and self.lonelyRoad[1] == "P":
            xStart = self.x - data.intersecRad//2
            yStart = self.y + data.intersecRad//2
            xEnd = xStart + data.intersecRad
            yEnd =  yStart 
        elif self.lonelyRoad[0].dir == [0,1] and self.lonelyRoad[1] == "N":
            xStart = self.x + data.intersecRad//2
            yStart = self.y - data.intersecRad//2
            xEnd = xStart - data.intersecRad
            yEnd =  yStart 
        canvas.create_line(xStart, yStart, xEnd, yEnd, fill = "white")
        