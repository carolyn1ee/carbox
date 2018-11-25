from roads import *
#from simulation import *
class SideRoad (Road):
    def __init__ (self, data, dir, xN, yN, xP, yP,\
                      secsBtCars, carsListN=None, carsListP=None, speedLimit = 5):
        super().__init__(data, dir, xN, yN, xP, yP,\
                    carsListN, carsListP, speedLimit)
        self.secsBtCars = secsBtCars
        # self.setExitLights (data)

        
    def addCarsPeriodically (self, data):
        if self.dir == [0,1]:
            if self.yN == 0:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInN(data, self.speedLimit)
            if self.yP == data.height:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInP(data, self.speedLimit)
                    
        if self.dir == [1,0]:
            if self.xN == 0:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInN(data, self.speedLimit)
            if self.xP == data.width:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInP(data, self.speedLimit)  
    # # allows it to always be green on the sides so the cars can leave
    # # def setExitLights (self, data):
    # #     if self.dir == [0,1]:
    # #         if self.yN == 0:
    # #             self.lightN = 1
    # #         if self.yP == data.height:
    # #                 self.lightP = 1
    # #     if self.dir == [1,0]:
    # #         if self.xN == 0:
    # #                self.lightN = 1
    # #         if self.xP == data.width:
    # #                 self.lightP = 1
    # #     

    def timerFiredRoad (self, data):
        # self.setExitLights (data)
        super().timerFiredRoad (data)
        if data.go:
            self.addCarsPeriodically (data)
 
    def __repr__ (self):
         return "sideRoad start: (" + str (self.xN )+ ", " + str(self.yN) + "); end: (" + str(self.xP) + ", " + str(self.yP) + "), direction: " + str(self.dir)
                      #essentially same as a normal road but creates cars on the edge
    
        