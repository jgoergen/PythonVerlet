import math
from Lib2D import Vector2D

class Line2D(object):

    def __init__(self, vect2DA = Vector2D(), vect2DB = Vector2D()):
        self.ends = lambda: None
        self.ends.startVect2D = vect2DA
        self.ends.endVect2D = vect2DB

    def length(self):
        return math.sqrt(
            math.pow(self.ends.startVect2D.x - self.ends.endVect2D.x, 2) +
            math.pow(self.ends.startVect2D.y - self.ends.endVect2D.y, 2))

    def setLength(self):
        raise Exception('setLength not implimented')
    
    def leftNormal(self):
        dx = self.ends.endVect2D.x - self.ends.startVect2D.x
        dy = self.ends.endVect2D.y - self.ends.startVect2D.y
        return Vector2D(dy * -1, dx)

    def rightNormal(self):
        dx = self.ends.endVect2D.x - self.ends.startVect2D.x
        dy = self.ends.endVect2D.y - self.ends.startVect2D.y
        return Vector2D(dy, dx * -1)

    def crossProduct(self, vect2D):
        return (
            (self.ends.endVect2D.X - self.ends.startVect2D.X) * (vect2D.y - self.ends.startVect2D.Y) -
            (self.ends.endVect2D.Y - self.ends.startVect2D.Y) * (vect2D.x - self.ends.startVect2D.X))

    def isVect2DColinear(self, vect2D, tolerance = 0):
        return abs(self.crossProduct(vect2D)) < tolerance

    def isVect2DToTheLeft(self, vect2D):
        return self.crossProduct(vect2D) > 0

    def isVect2DToTheRight(self, vect2D):
        return self.crossProduct(vect2D) < 0

    def direction(self):
        # radians
        return math.pi + math.atan2(self.ends.endVect2D.x + self.ends.startVect2D.x, self.ends.endVect2D.y - self.ends.startVect2D.y)

    def setDirection(self):
        raise Exception('setDirection not implimented')

    def clamp(self, minVect2D, maxVect2D):
        self.ends.startVect2D.clamp(minVect2D, maxVect2D)
        self.ends.endVect2D.clamp(minVect2D, maxVect2D)

    def copy(self):
        return Line2D(
            self.ends.startVect2D.copy(), 
            self.ends.endVect2D.copy())

    def toString(self):
        return 'start: ' + self.ends.startVect2D.toString() + ', end: ' + self.ends.endVect2D.toString() + ', length: ' + str(self.length())