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

    @staticmethod
    def CircleCrossesLine(pointVect, lineStartVect, lineEndVect, circleRadius=1):
        # https://stackoverflow.com/questions/1073336/circle-line-segment-collision-detection-algorithm
        d = lineEndVect.getSubtractedFromVector(lineStartVect)
        f = lineStartVect.getSubtractedFromVector(pointVect)
        a = d.dotProduct(d)
        b = 2 * f.dotProduct(d)
        discriminant = b * b - 4 * a * (f.dotProduct(f) - circleRadius * circleRadius)

        if(discriminant < 0):
            return False
        else:
            discriminant = sqrt(discriminant)
            t1 = (-b - discriminant) / (2 * a)
            t2 = (-b + discriminant) / (2 * a)

            if(t1 >= 0 and t1 <= 1):
                return True

            if(t2 >= 0 and t2 <= 1):
                return True

            return False

    @ staticmethod
    def GetCircleCrossingLineCollision(circleVector2D, lineStartVector, lineEndVector, circleRadius=1):
        # todo: shouldn't this take the circle radius into account?

        lineDirection = lineStartVector.getSubtractedFromVector(lineEndVector).normalize()
        pointToStart = circleVector2D.getSubtractedFromVector(lineStartVector)
        dot = pointToStart.dotProduct(lineDirection)
        nearestPointOnLine = lineStartVector.getAddedToVector(lineDirection.getMultipliedByScalar(dot))
        collisionVector = circleVector2D.getSubtractedFromVector(nearestPointOnLine).normalize()
        # verlet is build around recalcing these things in multiple passes, so the response needs to be dulled
        # otherwise it appears 'jumpy'
        collisionVector.multiplyByScalar(0.5)

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
