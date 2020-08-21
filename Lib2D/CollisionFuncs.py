import math
import numbers
from Lib2D import Vector2D

class CollisionFuncs(object):

    @staticmethod
    def PointAndCircle():
        pass

    @staticmethod
    def CircleAndCircle():
        pass

    # https:#stackoverflow.com/questions/37224912/circle-line-segment-collision
    # maybe try this instead? https:#stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm

    @staticmethod
    def CircleCrossesLine(pointVect, lineStartVect, lineEndVect, circleRadius = 1):

        #print(pointVect.toString())
        #print(lineStartVect.toString())
        #print(lineEndVect.toString())
        #print(circleRadius)

        v1 = lineEndVect.getSubtractedFromVector(lineStartVect)
        v2 = lineStartVect.getSubtractedFromVector(pointVect)

        #print(v1.toString())
        #print(v2.toString())

        b = v1.dotProduct(v2)
        #print(b)
        c = 2 * (v1.x * v1.x + v1.y * v1.y)
        #print(c)
        b *= -2
        #print(b)
        d = math.sqrt(b * b - 2 * c * (v2.x * v2.x + v2.y * v2.y - circleRadius * circleRadius))

        #print('-----------------')

        # no intercept
        if (isinstance(d, numbers.Number)):
            return False

        # these represent the unit distance of point one and two on the line
        u1 = (b - d) / c
        u2 = (b + d) / c

        if ((u1 <= 1 and u1 >= 0)):
            return True

        if ((u2 <= 1 and u2 >= 0)):
            return True

        return False

    @staticmethod
    def GetCircleCrossingLineCollision(circleVector2D, lineStartVector, lineEndVector, circleRadius = 1):
        # todo: shouldn't this take the circle radius into account?

        lineDirection = lineStartVector.getSubtractedFromVector(lineEndVector).normalize()
        pointToStart = circleVector2D.getSubtractedFromVector(lineStartVector)
        dot = pointToStart.dotProduct(lineDirection)
        nearestPointOnLine = lineStartVector.getAddedToVector(lineDirection.getMultipliedByScalar(dot))
        collisionVector = circleVector2D.getSubtractedFromVector(nearestPointOnLine).normalize()

        t = None
        
        if (abs(lineStartVector.x - lineEndVector.x) > abs(lineStartVector.y - lineEndVector.y)):
            t = (circleVector2D.x - collisionVector.x - lineStartVector.x) / (lineEndVector.x - lineStartVector.x)
        else:
            t = (circleVector2D.y - collisionVector.y - lineStartVector.y) / (lineEndVector.y - lineStartVector.y)

        lambdaVal = 1 / (t * t + (1 - t) * (1 - t))

        return {
            'pointCollisionVector': collisionVector.getMultipliedByScalar(0.5),
            'lineStartCollisionVector': collisionVector.getMultipliedByScalar(1 - t).multiplyByScalar(0.5).multiplyByScalar(lambdaVal),
            'lineEndCollisionVector': collisionVector.getMultipliedByScalar(t).multiplyByScalar(0.5).multiplyByScalar(lambdaVal)
        }