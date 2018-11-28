# import tkinter as tk
# from PIL import ImageTk
# from PIL import Image
# 
# class SimpleApp(object):
#     def __init__(self, master, filename, **kwargs):
#         self.master = master
#         self.filename = filename
#         self.canvas = tk.Canvas(master, width=500, height=500)
#         self.canvas.pack()
# 
#         self.update = self.draw().__next__
#         master.after(100, self.update)
# 
#     def draw(self):
#         image = Image.open(self.filename)
#         angle = 0
#         while True:
#             tkimage = ImageTk.PhotoImage(image.rotate(angle))
#             canvas_obj = self.canvas.create_image(
#                 250, 250, image=tkimage)
#             self.master.after_idle(self.update)
#             yield
#             self.canvas.delete(canvas_obj)
#             angle += 10
#             angle %= 360
# 
# root = tk.Tk()
# app = SimpleApp(root, 'imgs/imageCarWE.gif')
# root.mainloop()
# 
# # https://stackoverflow.com/questions/15736530/python-tkinter-rotate-image-animation

from roads import *
from sideRoads import *
from intersections import *
from sideIntersections import *
from threeWayIntersec import *
from Simulator import *

class Struct(object): pass
data = Struct()
# data.width = width
# data.height = height
# data.timerDelay = 100 # milliseconds
# # root = Tk()
# # root.resizable(width=False, height=False) # prevents resizing window
# init(data, roads, intersecs, set)
# if not data.set:
#     setTheLights(data, lights)
# # create the root and the canvas
# canvas = Canvas(root, width=data.width, height=data.height)
# canvas.configure(bd=0, highlightthickness=0)
# canvas.pack()
# # set up events
# root.bind("<Button-1>", lambda event:
#                         mousePressedWrapper(event, canvas, data))
# root.bind("<Key>", lambda event:
#                         keyPressedWrapper(event, canvas, data))
# timerFiredWrapper(canvas, data)
# # and launch the app
# root.mainloop()  # blocks until window is closed
# # if not data.set:
# #     return (SideIntersection.totalTimeWaiting, SideIntersection.totalCars, avgTimeSpentWaiting())
# # else:
# #     replaceIntersections(data)
# #     return (data.roads, data.intersecs)
# # print("bye!")



r1 = Road ( data, [0,1], 1, 2, 3, 4,\
                        carsListN=None, carsListP=None, speedLimit = 5)
r2 =  (r1.roadCopy())
print (r1)
print (r2)
print (r1 == r2)
s = {(r1, "P"), 5}
print ((r2, "P")  in s)
