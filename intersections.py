class Intersection (object):
    def __init__(self, data, listOfConnectedIntersections, x, y, listOfTimings):
        #list of connections is indexed in same way as list of timings
        #the first timing is the amount of time that the light is green from 
        self.listOfConnex = listOfConnectedIntersections
        self.listOfTimings = listOfTimings
        self.x = x
        self.y = y
        
       # write out the similarities between intersections and roads