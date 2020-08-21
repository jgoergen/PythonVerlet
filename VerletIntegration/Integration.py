import math
from Lib2D import Vector2D, CollisionFuncs

class Integration(object):

    def __init__(self, options):
        self.iterations = 2
        self.constraintSnapCallback = None
        self.useMass = False
        self.particles = []
        self.paused = False
        self.gravity = Vector2D(0, 0.005)
        self.constraints = []
        self.bodies = []
        self.stageMinVect = Vector2D(10, 10)
        self.stageMaxVect = Vector2D(790, 490)
        self.speedLimitMinVect = Vector2D(-4, -4)
        self.speedLimitMaxVect = Vector2D(4, 4)
        self.stageFriction = 0.001

        if (options is not None):
            if 'iterations' in options:
                self.iterations = options['iterations']

            if 'gravity' in options:
                self.gravity = options['gravity']

            if 'stageMinVect' in options:
                self.stageMinVect = options['stageMinVect']

            if 'stageMaxVect' in options:
                self.stageMaxVect = options['stageMaxVect']

            if 'speedLimitMinVect' in options:
                self.speedLimitMinVect = options['speedLimitMinVect']

            if 'speedLimitMaxVect' in options:
                self.speedLimitMaxVect = options['speedLimitMaxVect']

            if 'constraintSnapCallback' in options:
                self.constraintSnapCallback = options['constraintSnapCallback']

            if 'useMass' in options:
                self.useMass = options['useMass']

            if 'stageFriction' in options:
                self.stageFriction = options['stageFriction']

    def addParticle(self, particle):
        self.particles.append(particle)

    def addConstraint(self, constraint):
        self.constraints.append(constraint)

    def addBody(self, body):
        self.bodies.append(body)

    def runTimeStep(self, timeDelta = 0):
        if (self.paused is not True):
            self.runVerlet(timeDelta)
            self.satisfyConstraints()

    def runVerlet(self, timeDelta):
        # TODO
        # timeDeltaSquare = math.pow(timeDelta, 2)

        for i in range(0, len(self.particles)):
            # derive velocity
            velocityVector = self.particles[i].vector.getSubtractedFromVector(self.particles[i].lastVector)

            # apply gravity
            velocityVector.addToVector(self.gravity)

            # limit speed
            # velocityVector.clamp(speedLimitMinVect, speedLimitMaxVect)

            # adjust for timestep delta
            # velocityVector.multiplyBy(timeDeltaSquare)

            # apply stage friction
            velocityVector.multiplyByScalar(1 - self.stageFriction)

            # apply
            self.particles[i].lastVector = self.particles[i].vector.copy()
            self.particles[i].vector.addToVector(velocityVector)

    def satisfyConstraints(self):
        # clamp to stage
        for i in range(0, len(self.particles)):
            if (self.particles[i].radius is not None and self.particles[i].radius > 0):
                self.particles[i].vector.clamp(
                    self.stageMinVect.getAddedToScalar(self.particles[i].radius),
                    self.stageMaxVect.getSubtractedFromScalar(self.particles[i].radius))
            else:
                self.particles[i].vector.clamp(
                    self.stageMinVect,
                    self.stageMaxVect)
        
        for j in range(0, self.iterations):
            if (len(self.constraints) > 0):
                self.runConstraints()

            self.runParticleCollisions()
            
            if (len(self.constraints) > 0):
                self.runParticleOnLineCollisions()
                self.runBodyCollisions()
                self.runPinning()

    def runConstraints(self):
        for i in range(0, len(self.constraints)):
            # relationship constraints
            deltaVector = self.constraints[i].ends.startParticle.vector.getSubtractedFromVector(self.constraints[i].ends.endParticle.vector)
            deltalength = deltaVector.magnitude()
            diff = None
            invmass1 = None
            invmass2 = None

            if (self.useMass == True):
                invmass1 = self.constraints[i].ends.startParticle.mass * -1
                invmass2 = self.constraints[i].ends.endParticle.mass * -1
                diff = (self.constraints[i].rest - deltalength) / (deltalength * (invmass1 + invmass2))

            else:
                deltaVector.normalize()
                diff = (self.constraints[i].rest - deltalength)

            addVect2 = deltaVector.getMultipliedByScalar(diff)
            addVect3 = addVect2.copy()

            if (self.useMass == True):
                addVect2.multiplyBy(invmass2)

            # add stiffness calculation
            addVect3.multiplyByScalar(0.5).multiplyByScalar(self.constraints[i].stiffness)
            addVect2.multiplyByScalar(0.5).multiplyByScalar(self.constraints[i].stiffness)

            self.constraints[i].ends.startParticle.vector.addToVector(addVect3)
            self.constraints[i].ends.endParticle.vector.subtractByVector(addVect2)

            # snapping
            if (abs(diff) > self.constraints[i].tolerance):
                removedConstraint = self.constraints.pop(i)
                i = i - 1

                if (self.constraintSnapCallback is not None):
                    self.constraintSnapCallback(removedConstraint[0])

    def runParticleCollisions(self):
        totalRadius = 0

        for i in range(0, len(self.particles)):
            if (self.particles[i].collides is None or self.particles[i].collides is not True or self.particles[i].radius == 0):
                continue

            for o in range(0, len(self.particles)):
                if (self.particles[o].collides is None or self.particles[o].collides is not True or self.particles[o].radius == 0 or i == o):
                    continue

                totalRadius = (self.particles[i].radius + self.particles[o].radius)

                # first pass check for speed
                if (abs(self.particles[i].vector.x - self.particles[o].vector.x) > totalRadius or
                    abs(self.particles[i].vector.y - self.particles[o].vector.y) > totalRadius):
                    continue

                distance = self.particles[i].vector.distanceTo(self.particles[o].vector)
                
                if (distance < totalRadius):
                    collisionVector = self.particles[i].vector.getSubtractedFromVector(self.particles[o].vector).divideByScalar(distance)

                    if (self.useMass):
                        # slower but takes mass into account
                        collisionVector.multiplyByScalar(0.5)
                        dot1 = self.particles[i].vector.getSubtractedFromVector(self.particles[i].lastVector).dotProduct(collisionVector)
                        dot2 = self.particles[o].vector.getSubtractedFromVector(self.particles[o].lastVector).dotProduct(collisionVector)
                        optimizedP = 2.0 * (dot1 - dot2) / (self.particles[i].mass + self.particles[o].mass)

                        collisionVector.getMultipliedByScalar(optimizedP)
                        self.particles[o].vector.subtractByVector(collisionVector.getMultipliedByScalar(self.particles[i].mass))
                        self.particles[i].vector.addToVector(collisionVector.getMultipliedByScalar(self.particles[o].mass))
                    else:
                        # faster but ignores mass
                        collisionVector.multiplyByScalar(0.5)
                        self.particles[o].vector.subtractByVector(collisionVector)
                        self.particles[i].vector.addToVector(collisionVector)

    def runBodyCollisions(self):
        for i in range(0, len(self.bodies)):
            if (self.bodies[i].collides is not True):
                continue

            for o in range(0, len(self.bodies)):
                if (i != o and self.bodies[o].collides == True):
                    collisionData = self.bodies[i].getCollision(self.bodies[o])

                    if (collisionData is not None):
                        if (self.useMass == True):
                            # slower but takes mass into account
                            t = None

                            if (abs(collisionData['edge'].startParticle.vector.x - collisionData['edge'].endParticle.vector.x) > abs(collisionData['edge'].startParticle.vector.y - collisionData['edge'].endParticle.vector.y)):
                                t = (collisionData['vector'].x - collisionData['collisionVector'].x - collisionData['edge'].startParticle.vector.x) / (collisionData['edge'].endParticle.vector.x - collisionData['edge'].startParticle.vector.x)
                            else:
                                t = (collisionData['vector'].y - collisionData['collisionVector'].y - collisionData['zdge'].startParticle.vector.y) / (collisionData['edge'].endParticle.vector.y - collisionData['edge'].startParticle.vector.y)

                            lambdaVal = 1 / (t * t + (1 - t) * (1 - t))
                            edgeMass = t * collisionData['edgeBody'].mass + (1 - t) * collisionData['edgeBody'].mass
                            invCollisionMass = 1 / (edgeMass + collisionData['vectorBody'].mass)
                            ratio1 = collisionData['vectorBody'].mass * invCollisionMass
                            ratio2 = edgeMass * invCollisionMass
                            collisionData['edge'].startParticle.vector.subtractByVector(collisionData['collisionVector'].getMultipliedByScalar((1 - t) * ratio1 * lambdaVal))
                            collisionData['edge'].endParticle.vector.subtractByVector(collisionData['collisionVector'].getMultipliedByScalar(t * ratio1 * lambdaVal))
                            collisionData['vector'].addToVector(collisionData['collisionVector'].getMultipliedByScalar(ratio2))

                        else:
                            # faster but ignores mass
                            t = None

                            if (abs(collisionData['edge'].startParticle.vector.x - collisionData['edge'].endParticle.vector.x) > abs(collisionData['edge'].startParticle.vector.y - collisionData['edge'].endParticle.vector.y)):
                                t = (collisionData['vector'].x - collisionData['collisionVector'].x - collisionData['edge'].startParticle.vector.x) / (collisionData['edge'].endParticle.vector.x - collisionData['edge'].startParticle.vector.x)
                            else:
                                t = (collisionData['vector'].y - collisionData['collisionVector'].y - collisionData['edge'].startParticle.vector.y) / (collisionData['edge'].endParticle.vector.y - collisionData['edge'].startParticle.vector.y)

                            lambdaVal = 1 / (t * t + (1 - t) * (1 - t))
                            collisionData['edge'].startParticle.vector.subtractByVector(collisionData['collisionVector'].getMultipliedByScalar(1 - t).multiplyByScalar(0.5).multiplyByScalar(lambdaVal))
                            collisionData['edge'].endParticle.vector.subtractByVector(collisionData['collisionVector'].getMultipliedByScalar(t).multiplyByScalar(0.5).multiplyByScalar(lambdaVal))
                            collisionData['vector'].addToVector(collisionData['collisionVector'].getMultipliedByScalar(0.5))

    def runParticleOnLineCollisions(self):
        # TODO: this should only be run on particles that are not connected to bodies!
        for i in range(0, len(self.particles)):
            if (self.particles[i].collides is None or self.particles[i].collides is False or self.particles[i].radius is None or self.particles[i].radius == 0):
                continue

            for o in range(0, len(self.constraints)):
                if (self.constraints[o].collides and 
                    self.particles[i].objectID != self.constraints[o].objectID and 
                    self.particles[i] != self.constraints[o].ends.startParticle and 
                    self.particles[i] != self.constraints[o].ends.endParticle):

                    if (CollisionFuncs.CircleCrossesLine(
                        self.particles[i].vector,
                        self.constraints[o].ends.startParticle.vector,
                        self.constraints[o].ends.endParticle.vector,
                        self.particles[i].radius)):

                        collisionData = CollisionFuncs.GetCircleCrossingLineCollision(
                            self.particles[i].vector, 
                            self.constraints[o].ends.startParticle.vector,
                            self.constraints[o].ends.endParticle.vector,
                            self.particles[i].radius)

                        self.constraints[o].ends.startParticle.vector.subtractByVector(collisionData['lineStartCollisionVector'])
                        self.constraints[o].ends.endParticle.vector.subtractByVector(collisionData['lineEndCollisionVector'])
                        self.particles[i].vector.addToVector(collisionData['pointCollisionVector'])

    def runPinning(self):
        for i in range(0, len(self.particles)):
            if (self.particles[i].pinnedTo is not None):
                self.particles[i].vector = self.particles[i].pinnedTo.copy()