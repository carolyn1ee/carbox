#from simulation import *
from roads import *
        # has a list of the roads that run thru it and can control what cars go thru for each intersection. just makes all the parallel ones go simultaneously. if it is not 4way then teh roads can handle moving the cars right or left. otherwise, the cars are only going to go straight.
        
        # there are only 1 or 2 roads in roadsNS or roads EW....
        
        
        # needs to handle the cars that are going through the intersection: picks them up as they enter intersection and then drops them off as they go into next road.
class Intersection (Road):
    #optimizer will change the time for the lights
    def __init__(self, data, x, y, NSTime=7, EWTime=6, staggerTime=1, roadsNS=None,
                                        roadsEW=None):
                                            
        #roadsNS is a list of lists where the first element of the list is the road and the second element is which side of the road is in this intersection (P[ositive] or N[egative])
        self.roadsNS = roadsNS
        self.roadsEW = roadsEW
        if self.roadsNS == None:
            self.roadsNS = []
        if self.roadsEW == None:
            self.roadsEW =[]
        self.NSTime = NSTime
        self.EWTime = EWTime
        self.x = x
        self.y = y
        self.cycle = self.NSTime + self.EWTime + 2*data.yellowTime
        
        #sometimes you don't want to start with NS being green. sometimes, want
        #to stagger the times 
        self.staggerTime = staggerTime
        self.carsEW = []
        self.carsWE = []
        self.carsNS = []
        self.carsSN = []
        
        self.lightEW = 1
        self.lightNS = 0
        self.data = data
        
  
    #creates a set containing 2-tuples to replace a list full of 2-element lists.
    def listOfListsToSetOfTuples (self, lst):
        s = set ([])
        for l in lst:
            s.add ((l[0], l[1]))
        return s
      #copying RoadsList is the list of roads like NS and roads is a list of roads that have already been copied and that i want to alias in. need to find which roads from the aliasing roads that i should put in for say NS. this way, we have same roads across all intersections
    def copyRoadsList (self, copyingRoadsList, roads):
        l = []
        copyRoads = self.listOfListsToSetOfTuples (copyingRoadsList)
        #print ("copying Roads list: " + str(copyRoads) +"\n\n\n\n")
        #print ("big list of roads want to alias" + str(roads) + "\n\n\n\n")
        for r in roads:
            if ((r, "P")) in copyRoads:
                l += [[r, "P"]]
            if ((r, "N")) in copyRoads:
                l += [[r, "N"]]
        return l
    def intersecCopy (self, roads):
        return Intersection (self.data, self.x, self.y, self.NSTime, self.EWTime, self.staggerTime, self.copyRoadsList(self.roadsNS, roads), self.copyRoadsList(self.roadsEW, roads))
    def changeLights (self, roadsList, light):
        for road in roadsList:
            #need to check which side of the road is in this intersection
            if road[1] == "P":
                road[0].lightP = light
                #look at this for debugging: the number of times the
                # lights are being changed isn't correct -- that is prob why 
                #the cars aren't able to go thru.
            elif road [1] == "N":
                road[0].lightN = light
    
    def checkLights (self, data):
        self.cycle = self.NSTime + self.EWTime + 2*data.yellowTime
        if self.timerIsNSecs (data, self.cycle, self.staggerTime):
            self.lightNS = 1
            self.lightEW = 0
        elif self.timerIsNSecs (data, self.cycle, self.NSTime + self.staggerTime):
            self.lightNS = 2
            self.lightEW = 0
        elif self.timerIsNSecs (data, self.cycle, data.yellowTime + \
                            self.NSTime + self.staggerTime):
            self.lightNS = 0
            self.lightEW = 1
        elif self.timerIsNSecs (data, self.cycle, (self.EWTime + data.yellowTime + \
                            self.NSTime + self.staggerTime)):
            self.lightNS = 0
            self.lightEW = 2
           
        self.changeLights (self.roadsNS, self.lightNS)
        self.changeLights (self.roadsEW, self.lightEW)
    def stopLightImg (self, data, light):
        if light == 1:
            return data.greenLightImg
        elif light == 0: 
            return data.redLightImg
        else:
            return data.yellowLightImg
    def drawLightNS (self, data, canvas):
        canvas.create_image (self.x, self.y-40, image = self.stopLightImg (data, self.lightNS))
        canvas.create_text (self.x, self.y-40, text = self.NSTime)
    def drawLightEW (self, data, canvas):
        canvas.create_image (self.x-40, self.y, image = self.stopLightImg (data, self.lightEW))
        canvas.create_text (self.x-40, self.y, text = self.EWTime)
     #returns the road in the roadsList that isn't the nonroad   
    def otherRoad (self, roadsList, nonRoad):
        for road in roadsList:
            if road != nonRoad:
                return road
                 
    #handle cars coming thru the intersection:
        #takes cars that are coming into the intersection so that it can deal w/
    def pickUpCars (self, data):
        for road in self.roadsNS:
            if road [1] == "P":
                #check the road that is in the same direction but not this road isn't full
                ## just em make a function that returns a undamaged list without a given element...
                tmpCar = road[0].carOutP(data)
                if tmpCar != None and tmpCar != road [0].frontCarP:
                    if not self.otherRoad(self.roadsNS, road)[0].allFull ("P", data):
                        if (not tmpCar.movable and (road[0].lightP == 1) or road [0].lightP == 2) or (tmpCar.movable):
                            tmpCar.color = "red"
                            tmpCar.movable = True
                            self.carsNS += [tmpCar]
                            road[0].carsListP.remove (tmpCar)
                    else:
                        tmpCar.movable = False
            elif road [1] == "N":
                tmpCar = road[0].carOutN(data)
                if tmpCar != None and tmpCar != road [0].frontCarN:
                    if not self.otherRoad(self.roadsNS, road)[0].allFull ("N", data):
                        if (not tmpCar.movable and (road[0].lightN == 1) or road [0].lightN == 2) or (tmpCar.movable):
                            tmpCar.color = "red"
                            tmpCar.movable = True
                            self.carsSN += [tmpCar]
                            road[0].carsListN.remove (tmpCar)
                    else:
                        tmpCar.movable = False
        for road in self.roadsEW:
            if road [1] == "P":
                tmpCar = road[0].carOutP(data)
                if tmpCar != None and tmpCar != road [0].frontCarP:
                    if not self.otherRoad(self.roadsEW, road)[0].allFull ("P", data):
                        if (not tmpCar.movable and (road[0].lightP == 1) or road [0].lightP == 2) or (tmpCar.movable):
                            tmpCar.color = "red"
                            tmpCar.movable = True
                            self.carsWE += [tmpCar]
                            road[0].carsListP.remove (tmpCar)
                    else:
                        tmpCar.movable = False
            elif road [1] == "N":
                tmpCar = road[0].carOutN(data)
                if tmpCar != None and tmpCar != road [0].frontCarN:
                    if not self.otherRoad(self.roadsEW, road)[0].allFull ("N", data):
                        if (not tmpCar.movable and (road[0].lightN == 1) or road [0].lightN == 2) or (tmpCar.movable):
                            tmpCar.color = "red"
                            tmpCar.movable = True
                            self.carsEW += [tmpCar]
                            road[0].carsListN.remove (tmpCar)
                    else:
                        tmpCar.movable = False
            ###may have issues because the road will continue to try to accelerate the front car....
            
            ###may have issues because threeway doesnt have an opposite road prob fine
    def dropOffCars (self, data):
        for road in self.roadsNS:
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
        if data.t % 5 == 0:
            self.changeAccelAllCars()
            self.moveCars()
        self.checkLights(data)
        #snag cars coming into intersec
        #have some way to draw the cars... pretty similar to the road:
            #1) move cars
            #2) accelerate cars
            #3) once cars get out of intersection, send them to next intersection
    def countNumRoads (self):
        return len(self.roadsEW) + len (self.roadsNS)
            
    def __repr__ (self):
        return "(" + str(self.x) +"," + str(self.y) +"), light NS:" +str (self.lightNS) + \
        "light EW" + str (self.lightEW) + str (self.roadsNS) +str(self.roadsEW) + str (id (self)) +"\n\n\n\n\n"
##view
     #draws cars in the intersection   
    def drawIntersecCars (self, canvas):
        for carsList in [self.carsNS, self.carsSN, self.carsEW, self.carsWE]:
            for car in carsList:
                car.draw(canvas)
                # canvas.create_oval  (car.x - 20, car.y -20, car.x +30, car.y + 20, fill = car.color)
                # canvas.create_oval  (car.x - 30, car.y , car.x +30, car.y + 20, fill = "yellow")
                
    def drawAllIntersec (self, data, canvas):
        self.drawIntersecCars (canvas)
        self.drawLightEW (data, canvas)
        self.drawLightNS (data, canvas)