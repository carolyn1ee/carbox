from carClass import *
import random
class Road (object):
    #yP is the lower (more positive end). xP is the rightmost part 
        # (more positive). 
    #yN is the top of the road (more negative) and yN is the leftmost part of 
        #the road (more negative)
    
    #we have cars that go forward along the road and cars that go backwards. 
    #cars that go towards teh end of the road are going in positive direction
    #so they are carsListP and the opp direction cars are in carsListN
    
    #direction can be either [1,0] or [0,1] for whether or not it runs from vert
    #or hor.
    def __init__ (self, data, dir, xN, yN, xP, yP,\
                        carsListN=None, carsListP=None, speedLimit=3):
        #location:
        self.xN = xN
        self.yN = yN
        self.xP = xP
        self.yP = yP
        self.dir = dir
        #cars inside
        self.carsListN = carsListN
        self.carsListP = carsListP
        if self.carsListN == None:
            self.carsListN = []
        if self.carsListP == None:
            self.carsListP =[]
        #view
        self.ylowStripsLen = 10
        self.length = ((xN-xP)**2 + (yN-yP)**2)**.5
        #intersection
        self.lightN = 0
        self.lightP = 0
        self.frontCarN = None
        self.frontCarP = None
        self.speedLimit = speedLimit
        self.decelN = False
        self.decelP = False
        self.data = data
        
    ##standard functions:
    def __eq__ (self, other):
        return isinstance(other, Road) and other.xN == self.xN and other.yN == self.yN and other.xP == self.xP and other.yP == self.yP and other.dir == self.dir
    def __repr__ (self):
        return "start: (" + str (self.xN )+ ", " + str(self.yN) + "); end: (" + str(self.xP) + ", " + str(self.yP) + "), direction: " + str(self.dir) + super().__repr__()
    def copyCarList (self, carList):
        l = []
        for i in carList:
            l += [i.carCopy()]
        return l
    def roadCopy (self):
        return Road (self.data, self.dir, self.xN, self.yN, self.xP, self.yP,\
                        carsListN = None, carsListP = None, speedLimit = self.speedLimit)
    def __hash__(self):
        return hash((self.xN, self.yN, self.xP, self.yP, tuple(self.dir)))
##timerFiredF'ns:
    def moveCars (self, timer):
        for car in self.carsListN:
            if car.movable:
                car.move()
            car.keepTrackOfTime(timer)
        for car in self.carsListP:
            if car.movable:
                car.move()
            car.keepTrackOfTime(timer)
    def timerIsNSecs (self, data, m, n=0):
        #timerFired goes off 10 times per sec
        firesPerSec = 10 
        return data.t % (firesPerSec * m) == (n*firesPerSec) % (firesPerSec * m)
    ##intersections:
#given direction ("NS" etc) of carlist returns the first car object that is 
#in front of the intersection and in front enough that it can stop 
#before intersection
    def frontOfQueue (self, data, dir):
        if dir == [0,1]:
            for car in self.carsListP:
                if not car.movable:
                    return car
            for car in self.carsListP:
                if car.y < self.yP - data.intersecRad - car.buffer():
                    return car
        elif dir ==[0,-1]:
            for car in self.carsListN:
                if not car.movable:
                    return car
            for car in self.carsListN:
                if car.y > self.yN + data.intersecRad + car.buffer():
                    return car
        elif dir == [-1,0]:
            for car in self.carsListN:
                if not car.movable:
                    return car
            for car in self.carsListN:
                if car.x > self.xN + data.intersecRad + car.buffer():
                    return car
        elif dir == [1,0]:
            for car in self.carsListP:
                if not car.movable:
                    return car
            for car in self.carsListP:
                if car.x < self.xP  - data.intersecRad - car.buffer():
                    return car
#checks if it is close enough to the intersection to start to slow down the car
    def inSlowArea (self, data, car):
        if car == None:
            return False
        buffer = car.buffer()
        if car.dir == [0,1]:
            return car.y > self.yP -buffer - data.intersecRad
        elif car.dir == [0,-1]:
            return car.y < self.yN + buffer + data.intersecRad
        elif car.dir == [1, 0]:
            return car.x > self.xP - buffer - data.intersecRad
        elif car.dir == [-1,0]:
            return car.x < self.xN +buffer +data.intersecRad


#control cars
    def setFrontCar(self, data):
        #NS
        if self.dir == [0,1]:
            if self.frontCarN == None:
                self.frontCarN = self.frontOfQueue (data, [0,-1])
            if self.frontCarP == None:
                self.frontCarP = self.frontOfQueue (data, [0,1])
        #EW
        elif self.dir == [1,0]:
            if self.frontCarN == None:
                self.frontCarN = self.frontOfQueue (data, [-1,0])
            if self.frontCarP == None:
                self.frontCarP = self.frontOfQueue (data, [1,0])
    #decelerate front car if the light is red or yellow
# maybe you are messing up if you are not setting the front car before 
#trying to slow down the front car (fix this by checking inSlowArea to make sure
# your car isn't None.
    def slowFrontIfYellRed(self, data):
        if (self.lightN == 0 or self.lightN == 2) and self.carsListN != []:
            if self.inSlowArea (data, self.frontCarN) or self.decelN:
                self.decelN = True
                self.frontCarN.deceler()
        if (self.lightP == 0 or self.lightP == 2) and self.carsListP != []:
            if self.inSlowArea(data, self.frontCarP) or self.decelP:
                self.decelP = True
                self.frontCarP.deceler()
    #let's you know if there are cars all backed up all the way so the intersection doesn't add any more cars in
    def allFull (self, end, data):
        margin = 100 #need a bit more room for the cars coming in to stop
        if self.dir == [0,1] and end == "P":
            for car in self.carsListN:
                if car.y > self.yP - data.intersecRad - margin and car.curSpeed == 0:
                    car.color = "purple"
                    return True
        if self.dir == [0,1] and end == "N":
            for car in self.carsListP:
                if car.y < self.yN + data.intersecRad+margin and car.curSpeed == 0:
                    car.color = "purple"
                    return True
        if self.dir == [1,0] and end == "P":
            for car in self.carsListN:
                if car.x > self.xP - data.intersecRad-margin and car.curSpeed == 0:
                    car.color = "purple"
                    return True
        if self.dir == [1,0] and end == "N":
            for car in self.carsListP:
                if car.x < self.xN + data.intersecRad+margin and car.curSpeed == 0:
                    car.color = "purple"
                    return True
        return False
    #make sure cars have space bt each other by decelerating close cars
    def changeAccelCars (self, data):
        for c in range(1, len(self.carsListN)):
            car1 = self.carsListN [c]
            for lead in range (0, c):
                car2 = self.carsListN [lead]
                car1.decelerating = False
                #checks every car that is in front of this car jic you run over a car....
                if car1.isTooClose (car2):
                    car1.deceler()
                    car1.decelerating = True
                    if car1.hasCrashed(car2):
                        data.crashes += 1
            if not(car1 == self.frontCarN) and not car1.decelerating and car1.movable:
                car1.acceler()
        if self.carsListN != [] and not(self.carsListN [0] == self.frontCarN) and self.carsListN [0].movable:
            self.carsListN [0].acceler()
        for c in range(1, len(self.carsListP)):
            car1 = self.carsListP [c]
            for lead in range (0, c):
                car2 = self.carsListP [c-1]
                car1.decelerating = False
                if car1.isTooClose (car2):
                    if car1.hasCrashed(car2):
                        data.crashes += 1
                    car1.deceler()
                    car1.decelerating = True
            if not(car1 == self.frontCarP) and not car1.decelerating and car1.movable:
                car1.acceler()
        if self.carsListP != [] and not (self.carsListP [0] == self.frontCarP) and self.carsListP [0].movable:
            self.carsListP [0].acceler()
###some methods for intersection to call
# intersection will call on this function in timerFired when the light is green to grab the 
#car falling out of the intersection. then the intersection will have control 
#of the car (deletes car from this road and adds it to an intersection list of 
#cars (but only if there is a car falling out)) and intersection moves the car
#to the next road (adds car to next road)
    def carOutN (self, data):
        ## if self.carsListN != []:
            
            #vert road case
        if self.dir == [0,1]:
            for car in self.carsListN:
                if not car.movable:
                    # car.color = "pink"
                    return car
            for car in self.carsListN:
                if car.y < self.yN + data.intersecRad:
                    car.t = random.randint (0,1)#assign a turning direction 
                    #even if not in a threeway
                    # car.color = "pink"
                    return car
            #hor road case
        elif self.dir == [1,0]:
            for car in self.carsListN:
                if not car.movable:
                    # car.color = "pink"
                    return car
            for car in self.carsListN:
                if car.x < self.xN + data.intersecRad:
                    car.t = random.randint (0,1)
                    # car.color = "pink"
                    return car
    def carOutP (self, data):
        ##if self.carsListP != []:
        #now is returning any car that isn't too far in the intersection
        # but it should be the first car that is too far anyways
        
            #vert road case
        if self.dir == [0,1]:
            for car in self.carsListP:
                if not car.movable: #if the car had gotten stuck by intersection, need to make sure it is given the opportunity to get out of the intersection. want to check its movability before positioning because the ones that are stuck are going to block up all the ones behind
                    return car
            for car in self.carsListP:
                if car.y > self.yP - data.intersecRad:
                    car.t = random.randint (0,1) 
                    return car
            #hor road case
        elif self.dir == [1,0]:
            for car in self.carsListP:
                if not car.movable:
                    return car
            for car in self.carsListP:
                if car.x > self.xP - data.intersecRad:
                    car.t = random.randint (0,1)
                    return car
    #add a car into the road going from P to N (ie a negative car) but it is
    # entering the positive side of the road.
    def carInP (self, data, curSpeed):
        #vert
        if self.dir == [0,1]:
            carDir = [0,-1]
            carX = self.xN + Car.width//2
            carY = self.yP - data.intersecRad
        #hor
        elif self.dir == [1,0]:
            carDir = [-1,0]
            carY = self.yN - Car.width//2
            carX = self.xP - data.intersecRad
        car = Car (data, self.speedLimit, curSpeed, carDir, carX, carY)
        self.carsListN += [car]
        
    def carInN (self, data, curSpeed):
        #vert
        if self.dir == [0,1]:
            carDir = [0,1]
            carX = self.xP - Car.width//2
            carY = self.yN + data.intersecRad
        #hor
        elif self.dir == [1,0]:
            carDir = [1,0]
            carY = self.yN + Car.width//2
            carX = self.xN + data.intersecRad
        car = Car (data, self.speedLimit, curSpeed, carDir, carX, carY)
        self.carsListP += [car]

#call this in simulation in timerFired
    def timerFiredRoad (self, data, timer):
        self.moveCars(timer)
        self.setFrontCar (data)
        if self.lightN == 1:
            self.frontCarN = None
            self.decelN = False
        if self.lightP == 1:
            self.frontCarP = None
            self.decelP = False
        self.slowFrontIfYellRed (data)
        self.changeAccelCars (data)
        
##view functions    
    def drawRoad(self, canvas, data):
        lenOfRoadNeedingStrips = (self.length - 2*data.intersecRad)
        for strip in range \
                (int(lenOfRoadNeedingStrips//self.ylowStripsLen-1)):
            if strip % 2 == 0:
                startX = data.intersecRad * self.dir[0] + self.xN + \
                    strip*self.ylowStripsLen * self.dir[0]
                startY = data.intersecRad * self.dir [1] + self.yN + \
                    strip*self.ylowStripsLen*self.dir[1]
                endX = data.intersecRad * self.dir [0] + self.xN + \
                    (strip + 1)*self.ylowStripsLen * self.dir[0]
                endY = data.intersecRad * self.dir[1] + self.yN + (strip +\
                    1)*self.ylowStripsLen*self.dir[1]
                canvas.create_line(startX, startY, endX, endY, width= 5, fill = "yellow")
                xCarMargin = Car.width * self.dir[1]
                yCarMargin = Car.width * self.dir[0]
                xIntersecMargin = data.intersecRad//2 * self.dir[0]
                yIntersecMargin = data.intersecRad//2 * self.dir [1]
        canvas.create_line (self.xN + xCarMargin + xIntersecMargin, 
                            self.yN + yCarMargin + yIntersecMargin , 
                            self.xP + xCarMargin - xIntersecMargin, 
                            self.yP + yCarMargin - yIntersecMargin, fill = "white")
        canvas.create_line (self.xN - xCarMargin + xIntersecMargin, 
                            self.yN - yCarMargin + yIntersecMargin, 
                            self.xP - xCarMargin - xIntersecMargin, 
                            self.yP - yCarMargin - yIntersecMargin, fill = "white")
    def drawCars (self, canvas, data):
        if self.dir == [0,1]:
            color = "red"
        else:
            color = "blue"
        for car in self.carsListN:
            car.draw(canvas)
            canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = car.color)
            # if car is self.frontCarN:
            #     canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = "white")
            if not car.movable:
                canvas.create_rectangle  (car.x , car.y - 20, car.x +20, car.y + 20, fill = "green")
        for car in self.carsListP:
            car.draw(canvas)
            canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = car.color)
            # if car is self.frontCarP:
            #     canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = "white")
            if not car.movable:
                canvas.create_rectangle  (car.x , car.y - 20, car.x +20, car.y + 20, fill = "green")
                
    def drawAllRoad (self, canvas, data):
        self.drawRoad (canvas, data)
        self.drawCars (canvas, data)
        

##
