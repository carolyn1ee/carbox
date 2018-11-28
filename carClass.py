import random 
from tkinter import *
from image_util import *
from PIL import ImageTk,Image  
    
class Car(object): 
    #cite: syntax for images from https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python and from course website
    carImgNS = "imgs/imageCarNS.gif"
    carImgSN = "imgs/imageCarSN.gif"
    carImgEW = "imgs/imageCarEW.gif"
    carImgWE = "imgs/imageCarWE.gif"
    length = 40
    width = 20
    
    #direction is a list [x, y] ([1,0] means it goes from W to E; [0,1] means it goes from N to S)
    #t is the random variable that will store which direction this car decides to turn if it gets into an intersection.
    def __init__(self, data, speedLimit, curSpeed, direction, x, y, accel = 1, decel = 1, t = None):
        self.speedMax = speedLimit
        self.curSpeed = curSpeed
        self.dir = direction
        self.accel = accel
        self.decel = decel
        self.data = data
        self.x = x
        self.y = y
        #NS
        if self.dir == [0,1]:
            self.img = PhotoImage(file=Car.carImgNS)
        #SN
        elif self.dir == [0, -1]:
            self.img = PhotoImage(file=Car.carImgSN)
        #WE
        elif self.dir == [1,0]:
            self.img = PhotoImage(file=Car.carImgWE)
        #EW
        elif self.dir == [-1, 0]:
            self.img = PhotoImage(file=Car.carImgEW)
        self.t = t
        
        self.startTime = None
        self.totalTime = 0

    def copy (self):
        return Car (self.data, self.speedMax, self.curSpeed, self.dir, self.x, self.y, self.accel, self.decel, self.t)
         
    def draw (self, canvas):
        canvas.create_image(self.x, self.y, anchor = CENTER, image=self.img)  

    #checks all attributes are the same
    def __eq__ (self, other):
        return isinstance (other, Car) and other.curSpeed == self.curSpeed and \
        self.speedMax == other.speedMax and self.x == other.x and \
        self.y == other.y and self.accel == other.accel and self.decel == \
        other.decel
    
    def __repr__ (self):
        return str(self.dir) + "location: (" + str (self.x) + ", " + \
            str (self.y) +")" + "speed:" + str (self.curSpeed)
    def move (self):
        self.x += self.curSpeed * self.dir[0]
        self.y += self.curSpeed * self.dir[1]
    #makes the car decelerate up until stopped
    def deceler (self):
        if self.curSpeed >= self.decel:
            self.curSpeed -= self.decel
        else:
            self.curSpeed = 0
    #makes the car's speed increase up until the max speed
    
    def keepTrackOfTime (self, timer):
        if self.startTime == None and self.curSpeed == 0:
            self.startTime = timer
        elif self.curSpeed != 0 and self.startTime != None:
            self.totalTime += timer - self.startTime
            self.startTime = None
            
            
    def acceler (self):
        if self.curSpeed <= self.speedMax - self.accel:
            self.curSpeed +=  self.accel
        else:
            self.curSpeed = self.speedMax
    def countTimeWaiting (self):
        t = 0
        
    def isTooClose (self, other):
        return ((other.x-self.x)**2 + (other.y - self.y)**2)**.5 < self.buffer()
        
    def buffer (self):
        #used some nice physics to find out what distance ought to be to 
        #give the car enough space to stop
        return .5*self.curSpeed**2/self.decel + self.length