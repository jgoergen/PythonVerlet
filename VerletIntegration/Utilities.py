from math import pi, cos, sin


class Utilities(object):

    @staticmethod
    def RotatePoint(centerX, centerY, x, y, angleDegrees):
        radians = (pi / 180) * angleDegrees
        cosine = cos(radians)
        sine = sin(radians)
        nx = (cosine * (x - centerX)) + (sine * (y - centerY)) + centerX
        ny = (cosine * (y - centerY)) - (sine * (x - centerX)) + centerY
        return [nx, ny]
