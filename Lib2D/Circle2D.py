import math
from Lib2D import Vector2D

class Circle2D(object):

    def __init__(self, vect2D = Vector2D(), rad = 0):
        self.vector = vect2D
        self.radius = rad

    def isPointInside(self, x, y):
        return self.vector.distanceTo( Vector2D(x, y)) < self.radius

    def isVect2DInside(self, vect2D):
        return self.vector.distanceTo(vect2D) < self.radius

    def isCircleIntersecting(self, circle2D):
        distance = self.vector.distanceTo(circle2D.vector)
        return distance <= (self.radius + circle2D.radius)

    def isCircleInside(self, circle2D):
        distance = self.vector.distanceTo(circle2D.vector)

        if (circle2D.radius >= self.radius and distance <= (circle2D.radius - self.radius)):
            return True # circle 1 inside circle 2
        elif (self.radius >= circle2D.radius and distance <= (self.radius - circle2D.radius)):
            return True # circle 2 inside circle 1
        else:
            return False

    def copy(self):
        return  Circle2D(self.vector.copy(), self.radius)

    def toString(self):
        return self.vector.toString() + ', r: ' + str(self.radius)