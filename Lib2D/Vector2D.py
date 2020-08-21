import math  
from Lib2D import CachedMath

class Vector2D(object):

    NORMAL_TOLERANCE = 0.0001

    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y)
        

    def setMagnitude(self, magnitude):
        direction = self.direction()
        self.x = math.cos(direction) * magnitude
        self.y = math.sin(direction) * magnitude
        return self

    def length(self):
        return self.magnitude()

    def setLength(self, length):
        self.setMagnitude(length)
        return self

    def distanceTo(self, vector2D):
        return math.sqrt((vector2D.x - self.x) * (vector2D.x - self.x) + (vector2D.y - self.y) * (vector2D.y - self.y))

    def normalize(self):
        mag = self.magnitude()

        if (mag <= self.NORMAL_TOLERANCE):
            mag = 1

        self.x /= mag
        self.y /= mag

        if (abs(self.x) < self.NORMAL_TOLERANCE):
            self.x = 0

        if (abs(self.y) < self.NORMAL_TOLERANCE):
            self.y = 0

        return self

    def getNormalized(self):
        mag = self.magnitude()

        if (mag <= self.NORMAL_TOLERANCE):
            mag = 1

        x = self.x / mag
        y = self.y / mag

        if (abs(x) < self.NORMAL_TOLERANCE):
            self.x = 0

        if (abs(y) < self.NORMAL_TOLERANCE):
            self.y = 0

        return Vector2D(
            self.x / self.magnitude(), 
            self.y / self.magnitude())

    def getAddedToScalar(self, value):
        return Vector2D(
            self.x + value,
            self.y + value)

    def getAddedToVector(self, value):
        return Vector2D(
            self.x + value.x,
            self.y + value.y)

    def getSubtractedFromScalar(self, value):
        return Vector2D(
            self.x - value,
            self.y - value)

    def getSubtractedFromVector(self, value):
        return Vector2D(
            self.x - value.x,
            self.y - value.y)

    def getMultipliedByScalar(self, value):
        return Vector2D(
            self.x * value,
            self.y * value)

    def getMultipliedByVector(self, value):
        return Vector2D(
            self.x * value.x,
            self.y * value.y)

    def getDividedByScalar(self, value):
        try:
            return Vector2D(
                self.x / value,
                self.y / value)
        except:
            return self.copy()

    def getDividedByVector(self, value):
        try:
            return Vector2D(
                self.x / value.x,
                self.y / value.y)
        except:
            return self.copy()

    def addToScalar(self, value):
        self.x += value
        self.y += value
        return self

    def addToVector(self, value):
        self.x = self.x + value.x
        self.y = self.y + value.y
        return self

    def subtractByScalar(self, value):
        self.x -= value
        self.y -= value
        return self

    def subtractByVector(self, value):
        self.x -= value.x
        self.y -= value.y
        return self

    def multiplyByScalar(self, value):
        self.x *= value
        self.y *= value
        return self

    def multiplyByVector(self, value):
        self.x *= value.x
        self.y *= value.y
        return self

    def divideByScalar(self, value):
        try:
            self.x /= value
            self.y /= value
        except:
            pass

        return self

    def divideByVector(self, value):
        try:
            self.x /= value.x
            self.y /= value.y
        except:
            pass
            
        return self

    def dotProduct(self, value):
        return self.x * value.x + self.y * value.y

    def crossProduct(self, value):
        return self.x * value.y - value.x * self.y

    def reverse(self):
        self.x *= -1
        self.y *= -1
        return self

    def getReverse(self):
        return Vector2D(
            self.x * -1,
            self.y * -1)

    def direction(self): # radians
        return math.atan2(self.y, self.x)

    def setDirection(self, angle): # radians
        magnitude = self.magnitude()
        self.x = math.cos(angle) * magnitude
        self.y = math.sin(angle) * magnitude

    def getRightNormal(self):
        normal = self.getNormalized()
        return Vector2D(normal.y, -normal.x)

    def getLeftNormal(self):
        normal = self.getNormalized()
        return Vector2D(-normal.y, normal.x)

    def clamp(self, minVect2D, maxVect2D):
        # limit minimum
        if minVect2D is not None:
            if self.x < minVect2D.x:
                self.x = minVect2D.x

            if self.y < minVect2D.y:
                self.y = minVect2D.y

        # limit maximum
        if maxVect2D is not None:
            if self.x > maxVect2D.x:
                self.x = maxVect2D.x

            if self.y > maxVect2D.y:
                self.y = maxVect2D.y

        return self

    def copy(self):
        return Vector2D(self.x, self.y)
    
    def toString(self):
        return 'x:' + str(self.x) + ", y:" + str(self.y)