from math import sqrt
import numbers
from Lib2D import Vector2D


class CollisionFuncs(object):

    @staticmethod
    def PointAndCircle():
        pass

    @staticmethod
    def CircleAndCircle():
        pass

    # https:#stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm

    @staticmethod
    def newCircleCrossesLine(pointVect, lineStartVect, lineEndVect, circleRadius=1):
        # compute the triangle area times 2 (area = area2/2)
        area2 = abs((lineEndVect.x - lineStartVect.x) * (pointVect.y - lineStartVect.y) - (pointVect.x - lineStartVect.x) * (lineEndVect.y - lineEndVect.y))

        # compute the AB segment length
        LAB = sqrt((lineEndVect.x - lineStartVect.x) ** 2 + (lineEndVect.y - lineStartVect.y) ** 2)

        # compute the triangle height
        h = area2 / LAB

        # if the line intersects the circle
        if(h < circleRadius):
            return True
        else:
            return False

    # https:#stackoverflow.com/questions/37224912/circle-line-segment-collision

    @staticmethod
    def circleCrossesLine(pointVect, lineStartVect, lineEndVect, circleRadius=1):
        v1 = lineEndVect.getSubtractedFromVector(lineStartVect)
        v2 = lineStartVect.getSubtractedFromVector(pointVect)
        b = v1.dotProduct(v2)
        c = 2 * (v1.x * v1.x + v1.y * v1.y)
        b *= -2
        d = sqrt(b * b - 2 * c * (v2.x * v2.x + v2.y * v2.y - circleRadius * circleRadius))

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
    def GetCircleCrossingLineCollision(circleVector2D, lineStartVector, lineEndVector, circleRadius=1):
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
