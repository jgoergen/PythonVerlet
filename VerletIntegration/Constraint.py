import math
from Lib2D import Vector2D

class Constraint(object):

    def __init__(self, options):
        # particle1, particle2, newStiffness, newTolerance, doesCollide, objID, extraData
        self.ends = lambda: None
        self.ends.startParticle = options['startParticle']
        self.ends.endParticle = options['endParticle']
        self.data = options['data'] if 'data' in options else {}
        self.rest = self.ends.startParticle.vector.getSubtractedFromVector(self.ends.endParticle.vector).magnitude()
        self.stiffness = options['stiffness'] if 'stiffness' in options else 1
        self.tolerance = options['tolerance'] if 'tolerance' in options else 9999
        self.collides = options['collides'] if 'collides' in options else False
        self.objectID = options['objectID'] if 'objectID' in options else None

    def toString(self):
        print('rest: ' + str(self.rest) + ', stiffness: ' + str(self.stiffness) + ', tolerance: ' + str(self.tolerance))

        