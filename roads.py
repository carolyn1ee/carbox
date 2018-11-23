from carClass import *
class Road (object):
    #yP is the lower (more positive end). xP is the rightmost part 
        # (more positive). 
    #yN is the top of the road (more negative) and yN is the leftmost part of 
        #the road (more negative)
    
    #we have cars that go forward along the road and cars that go backwards. 
    #cars that go towards teh end of the road are going in positive direction
    #so they are carsListP and the opp direction cars are in carsListN
    
    # #lstSRds is a list of tuples where first element is the roads that 
    # #connect to the startxf of this road and second element is the side of the 
    # #connected road that is connected to this road 
    # i don't think i need list of the roads this connects to because 
    #intersection should handle that......
    
    #direction can be either [1,0] or [0,1] for whether or not it runs from vert
    #or hor.
    def __init__ (self, data, dir, xN, yN, xP, yP, lstSRds, lstERds,\
                    carsListN, carsListP):
        #location:
        self.xN = xN
        self.yN = yN
        self.xP = xP
        self.yP = yP
        self.dir = dir

        #connex
        self.lstSRds = lstSRds
        self.lstERds = lstERds
        #cars inside
        self.carsListN = carsListN
        self.carsListP = carsListP
        #aesthetics
        self.ylowStripsLen = 10
        self.length = ((xN-xP)**2 + (yN-yP)**2)**.5
        #intersection
        self.lightN = 0
        self.lightP = 0
        self.frontCarN = None
        self.frontCarP = None
        
##timerFiredF'ns:
    def moveCars (self):
        for car in self.carsListN:
            car.move()
        for car in self.carsListP:
            car.move()
            
    ##intersections:
#given direction ("NS" etc) of carlist returns the first car object that is 
#in front of the intersection and in front enough that it can stop 
#before intersection
    def frontOfQueue (self, data, dir):
        if dir == [0,1]:
            for car in self.carList:
                if car.y < self.yP - data.intersecRad - car.buffer():
                    return car
        elif dir ==[0,-1]:
            for car in carList:
                if car.y > self.yN + data.intersecRad + car.buffer():
                    return car
        elif dir == [-1,0]:
            for car in carList:
                if car.x > self.xN + data.intersecRad + car.buffer():
                    return car
        elif dir == [1,0]:
            for car in carList:
                if car.x < self.xP  - data.intersecRad - car.buffer():
                    return car
       
    def inSlowArea (self, data, car):
        buffer = car.buffer()
        if self.dir == [1,0]:
            return car.y > self.yP - buffer - data.intersecRad or \
                car.y < self.yN + buffer + data.intersecRad
        elif self.dir == [0,1]:
            return car.x > self.xP - buffer - data.intersecRad or \
                car.x < self.xN + buffer + data.intersecRad

#control cars
    def setFrontCar(self, data):
        #NS
        if self.dir == [0,1]:
            if self.frontCarN == None:
                self.frontCarN = self.frontOfQueue (self, data, [0,-1])
            if self.frontCarP == None:
                self.frontCarP = self.frontOfQueue (self, data, [0,1])
        #EW
        elif self.dir == [1,0]:
            if self.frontCarN == None:
                self.frontCarN = self.frontOfQueue (self, data, [-1,0])
            if self.frontCarP == None:
                self.frontCarP = self.frontOfQueue (self, data, [1,0])
    #decelerate car front car if the light is red or yellow
# maybe you are messing up if you are not setting the front car before 
#trying to slow down the front car (fix this by checking inSlowArea to make sure
# your car isn't None.
    def slowFrontIfYellRed(self, data):
        if self.lightN == 0 or self.lightN == 2:
            if inSlowArea(self, data, self.frontCarN):
                self.frontCarN.deceler()
        if self.lightP == 0 or self.lightP == 2:
            if inSlowArea(self, data, self.frontCarP):
                self.frontCarP.deceler()
                
    def distBtCars (self, car1, car2):
        return ((car1.x-car2.x)**2 + (car1.y-car2.y)**2)**.5
        
    def isTooClose (self, car1, car2):
        return self.distBtCars (car1, car2) < car1.buffer()
        
    #make sure cars have space bt each other by decelerating close cars
    def changeAccelCars (self):
        for c in range(1, len(self.carsListN)):
            if isTooClose (self.carsListN [c], self.carsListN [c-1]):
                self.carsListN[c].deceler()
            elif self.carsListN[c] != self.frontCarN:
                self.carsListN[c].acceler()
        if self.carsListN [0] != self.frontCarN:
            self.carsListN [0].acceler()
        for c in range(1, len(self.carsListP)):
            if isTooClose (self.carsListP [c], self.carsListP [c-1]):
                self.carsListP[c].deceler()
            elif self.carsListP[c] != self.frontCarP:
                self.carsListP[c].acceler()
        if self.carsListP [0] != self.frontCarP:
            self.carsListP [0].acceler()
###some methods for intersection to call
# intersection will call on this function in timerFired when the light is green to grab the 
#car falling out of the intersection. then the intersection will have control 
#of the car (deletes car from this road and adds it to an intersection list of 
#cars (but only if there is a car falling out)) and intersection moves the car
#to the next road (adds car to next road)
    def carOutN (self, data):
        #vert road case
        if self.dir == [0,1]:
            if self.carsListN[0].y < self.yN + data.intersecRad:
                return self.carsListN[0]
        #hor road case
        else:
            if self.carsListN[0].x< self.xN + data.intersecRad:
                return self.carsListN[0]
    def carOutP (self, data):
        #vert road case
        if self.dir == [0,1]:
            if self.carsListP[0].y > self.yN - data.intersecRad:
                return self.carsListP[0]
        #hor road case
        else:
            if self.carsListP[0].x > self.xN - data.intersecRad:
                return self.carsListP[0]
    #add a car into the road going from P to N (ie a negative car) but it is
    # entering the positive side of the road.
    def carInP (self, data, curSpeed):
        car = Car ()
        self.carsListN += car

#call this in simulation in timerFired
    def timerFiredRoad (self, data):
        self.moveCars()
        self.setFrontCar (data)
        if self.lightN == 1:
            self.frontCarN = None
        if self.lightP == 1:
            self.frontCarP = None
        self.slowFrontIfYellRed (data)
        self.changeAccelCars ()
        
    
        
        
##view functions
    def drawRoad(self, canvas, data):
        lenOfRoadNeedingStrips = (self.length - 2*data.intersecRad)
        for strip in range \
                (int(lenOfRoadNeedingStrips//self.ylowStripsLen-1)):
            if strip % 2 == 0:
                startX = data.intersecRad + self.xN + strip*self.ylowStripsLen * self.dir[0]
                startY = data.intersecRad + self.yN + strip*self.ylowStripsLen*self.dir[1]
                endX = data.intersecRad + self.xN + (strip + 1)*self.ylowStripsLen * self.dir[0]
                endY = data.intersecRad + self.yN + (strip + 1)*self.ylowStripsLen*self.dir[1]
                canvas.create_line(startX, startY, endX, endY, width= 5, fill = "yellow")
    def drawCars (self, canvas, data):
        for car in self.carsListN:
            car.draw(canvas)
        for car in self.carsListP:
            car.draw()
    def drawAllRoad (self, canvas, data):
        self.drawRoad (canvas, data)
        self.drawCars (canvas, data)
    
##controller functions
# put this somewhere else like in the simulation bc simulation will prob make the roads
#will use this to snap to the grid of 10 by 10 when creating roads
    def roundToTen(n):
        if n%10>=5:
            return n//10 * 10 + 10
        else:
            return n//10 * 10
    