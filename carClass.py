import random 
from tkinter import *
from image_util import *
from PIL import ImageTk,Image  


# root = Tk()      
# canvas = Canvas(root, width = 300, height = 300)      
# canvas.pack()   

   
class Car(object):
    #direction is a list [x, y] ([1,0] means it goes from W to E; [0,1] means it goes from N to S)
    carImgNS = "imgs/imageCarNS.gif"
    carImgSN = "imgs/imageCarSN.gif"
    carImgEW = "imgs/imageCarEW.gif"
    carImgWE = "imgs/imageCarWE.gif"

    def __init__(self, data, speedLimit, direction, accel, decel):
        self.length = 40
        self.speedMax = speedLimit
        self.curSpeed = self.speedMax
        self.dir = direction
        self.accel = accel
        self.decel = decel
        self.data = data
        #NS
        if self.dir [0] == 0 and self.dir [1] == 1:
            self.x = data.width // 2 - data.radius
            self.y = 0
            self.img = PhotoImage(file=Car.carImgNS)
        #SN
        elif self.dir [0] == 0 and self.dir [1] == -1:
            self.x = data.width // 2 + data.radius
            self.y = data.height
            self.img =  PhotoImage(file=Car.carImgSN)
        #WE
        elif self.dir [0] == 1 and self.dir [1] == 0:
            self.x = 0
            self.y = data.height // 2 + data.radius
            self.img =  PhotoImage(file=Car.carImgWE)
        #EW
        elif self.dir [0] == -1 and self.dir [1] == 0:
            self.x = data.width
            self.y = data.height // 2 - data.radius
            self.img =  PhotoImage(file=Car.carImgEW)
        
        #need to know in advance before the intersection if you are going to 
        #need to be slowing down once you get closer to intersection
        self.intersecSlow = False
    #got syntax for images from https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python
    
    
    def draw (self, canvas):
        canvas.create_image(self.x, self.y, image=self.img)  
    
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
        return .5*self.curSpeed**2/self.decel + self.length
