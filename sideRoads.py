from roads import *
#from simulation import *
class SideRoad (Road):
    def __init__ (self, data, dir, xN, yN, xP, yP,\
                      secsBtCars, carsListN=None, carsListP=None, speedLimit = 5):
        super().__init__(data, dir, xN, yN, xP, yP,\
                    carsListN, carsListP, speedLimit)
        self.secsBtCars = secsBtCars
    def __hash__ (self):
            return hash((self.xN, self.yN, self.xP, self.yP, tuple(self.dir), self.secsBtCars))

    def roadCopy (self):
        return SideRoad (self.data, self.dir, self.xN, self.yN, self.xP, \
                    self.yP, secsBtCars = self.secsBtCars, carsListN = None, \
                        carsListP= None, speedLimit = self.speedLimit)
    def addCarsPeriodically (self, data):
        if self.dir == [0,1]:
            if self.yN <= 0:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInN(data, self.speedLimit)
            if self.yP >= data.height:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInP(data, self.speedLimit)
                    
        if self.dir == [1,0]:
            if self.xN <= 0:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInN(data, self.speedLimit)
            if self.xP >= data.width:
                if self.timerIsNSecs (data, self.secsBtCars):
                    self.carInP(data, self.speedLimit)  

    def timerFiredRoad (self, data, timer):
        super().timerFiredRoad (data, timer)
        self.addCarsPeriodically (data)
    # def drawCars (self, canvas, data):
    #     if self.dir == [0,1]:
    #         color = "orange"
    #     else:
    #         color = "grey"
    #     for car in self.carsListN:
    #         car.draw(canvas)
    #         canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = color)
    #         if car is self.frontCarN:
    #             canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = "white")
    #         if not car.movable:
    #             canvas.create_rectangle  (car.x , car.y - 20, car.x +20, car.y + 20, fill = "green")
    #     for car in self.carsListP:
    #         car.draw(canvas)
    #         canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = color)
    #         if car is self.frontCarP:
    #             canvas.create_oval(car.x - 20, car.y - 20, car.x + 20, car.y + 20, fill = "white")
    #         if not car.movable:
    #             canvas.create_rectangle  (car.x , car.y - 20, car.x +20, car.y + 20, fill = "green")
        
    ####standard f'ns    
    def __eq__ (self, other):
        return isinstance(other, SideRoad) and other.xN == self.xN and other.yN == self.yN and other.xP == self.xP and other.yP == self.yP and other.dir == self.dir and other.secsBtCars == self.secsBtCars
    def __repr__ (self):
         return "sideRoad start: (" + str (self.xN )+ ", " + str(self.yN) + "); end: (" + str(self.xP) + ", " + str(self.yP) + "), direction: " + str(self.dir) + super().__repr__()
                      #essentially same as a normal road but creates cars on the edge
    
        