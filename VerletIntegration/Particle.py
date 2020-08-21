import math
from Lib2D import Vector2D

class Particle(object):

    def __init__(self, options):
        self.vector = options['vector'] if 'vector' in options else Vector2D()
        self.lastVector = self.vector.copy()
        self.mass = options['mass'] if 'mass' in options else 1
        self.pinnedTo = options['pinnedTo'] if 'pinnedTo' in options else None
        self.collides = options['collides'] if 'collides' in options else False
        self.objectID = options['objectID'] if 'objectID' in options else None
        self.data = options['data'] if 'data' in options else {}
        self.radius = options['radius'] if 'radius' in options else 0

    def toString(self):
        return 'vector: ' + self.vector.toString()