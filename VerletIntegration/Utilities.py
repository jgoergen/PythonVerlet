import math

class Utilities(object):

    @staticmethod
    def RotatePoint(centerX, centerY, x, y, angleDegrees):
        radians = (math.pi / 180) * angleDegrees
        cos = math.cos(radians)
        sin = math.sin(radians)
        nx = (cos * (x - centerX)) + (sin * (y - centerY)) + centerX
        ny = (cos * (y - centerY)) - (sin * (x - centerX)) + centerY
        return [nx, ny]