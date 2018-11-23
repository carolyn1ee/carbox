from roads import *
from simulation import *
class sideRoads (Road):
    def __init__ (self, data, dir, xN, yN, xP, yP,\
                    carsListN, carsListP, speedLimit, secsBtCars):
        super.__init__ (data, dir, xN, yN, xP, yP,\
                    carsListN, carsListP, speedLimit)
        self.secsBtCars = secsBtCars
    def addCarsPeriodically (self, data):
        if self.dir == [0,1]:
            if self.yN == 0:
                if timerIsNSecs (secsBtCars):
                    self.carInN()
            if self.yP == data.height:
                if timerIsNSecs (secsBtCars):
                    self.carInP()
        if self.dir == [1,0]:
            if self.xN == 0:
                if timerIsNSecs (secsBtCars):
                    self.carInN()
            if self.xP == data.width:
                if timerIsNSecs (secsBtCars):
                    self.carInP()  
                    
    def timerFiredRoad (self, data):
        super.timerFiredRoad (data)
        self.addCarsPeriodically (data)
                    
                    
                      #essentially same as a normal road but creates cars on the edge
    
    
    ## prob let's do side roads cuz dis same as de roads
    ##need to check cuz you're making road elements be like [road, N] and then you don't do anything about the indexing