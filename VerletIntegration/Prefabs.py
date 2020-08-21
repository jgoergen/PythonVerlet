import math, random
from Lib2D import Vector2D
from VerletIntegration import Utilities, Particle, Constraint, Body

class Prefabs(object):

    @staticmethod
    def Rope(verlet, startX, startY, links, linkLength, elasticity, pinFirst, objectID):
        lastParticle = None

        if (objectID is None):
            objectID = random.randint(0, 100000)

        for i in range(0, links):
            pin = Vector2D(startX, startY) if lastParticle == None and pinFirst == True else None

            particle = Particle({
                'vector': Vector2D(startX, startY),
                'pinnedTo': pin
            })

            verlet.addParticle(particle)

            if (lastParticle):
                verlet.addConstraint(
                    Constraint({
                        'startParticle': particle,
                        'endParticle': lastParticle,
                        'stiffness': elasticity,
                        'objectID': objectID,
                        'data': { 'drawn': True }
                    }))

            startX += linkLength
            lastParticle = particle

    @staticmethod
    def Box(verlet, x, y, width, height, rotationDegrees, collides, stiffness, objectID):
        from VerletIntegration import Utilities

        particle1 = Particle({
            'vector': Vector2D(x, y),
            'objectID': objectID,
            'collides': False
        })

        rotatedPoint1 = Utilities.RotatePoint(x, y, x + width, y, rotationDegrees)

        particle2 = Particle({
            'vector': 
                Vector2D(
                    rotatedPoint1[0],
                    rotatedPoint1[1]),
            'objectID': objectID,
            'collides': False
        })

        rotatedPoint2 = Utilities.RotatePoint(x, y, x + width, y + height, rotationDegrees)

        particle3 = Particle({
            'vector': 
                Vector2D(
                    rotatedPoint2[0],
                    rotatedPoint2[1]),
            'objectID': objectID,
            'collides': False
        })

        rotatedPoint3 = Utilities.RotatePoint(x, y, x, y + height, rotationDegrees)

        particle4 = Particle({
            'vector': 
                Vector2D(
                    rotatedPoint3[0],
                    rotatedPoint3[1]),
            'objectID': objectID,
            'collides': False
        })

        verlet.addParticle(particle1)
        verlet.addParticle(particle2)
        verlet.addParticle(particle3)
        verlet.addParticle(particle4)

        constraint1 = Constraint({
            'startParticle': particle1,
            'endParticle': particle2,
            'stiffness': stiffness,
            'objectID': objectID,
            'collides': collides,
            'data': { 'drawn': True }
        })

        verlet.addConstraint(constraint1)

        constraint2 = Constraint({
            'startParticle': particle2,
            'endParticle': particle3,
            'stiffness': stiffness,
            'objectID': objectID,
            'collides': collides,
            'data': { 'drawn': True }
        })

        verlet.addConstraint(constraint2)

        constraint3 = Constraint({
            'startParticle': particle3,
            'endParticle': particle4,
            'stiffness': stiffness,
            'objectID': objectID,
            'collides': collides,
            'data': { 'drawn': True }
        })

        verlet.addConstraint(constraint3)

        constraint4 = Constraint({
            'startParticle': particle4,
            'endParticle': particle1,
            'stiffness': stiffness,
            'objectID': objectID,
            'collides': collides,
            'data': { 'drawn': True }
        })

        verlet.addConstraint(constraint4)
        verlet.addBody(Body({
            'edges': [
                constraint1,
                constraint2,
                constraint3,
                constraint4
            ],
            'collides': True
        }))

        verlet.addConstraint(
            Constraint({
                'startParticle': particle1,
                'endParticle': particle3,
                'stiffness': stiffness,
                'objectID': objectID,
                'collides': False
            }))

        verlet.addConstraint(
            Constraint({
                'startParticle': particle2,
                'endParticle': particle4,
                'stiffness': stiffness,
                'objectID': objectID,
                'collides': False
            }))

    @staticmethod
    def Triangle(verlet, startX, startY, size, elasticity, objectIndex):

        particle1 = Particle({
            'vector': Vector2D(startX, startY),
            'collides': False
        })

        particle2 = Particle({
            'vector': Vector2D(startX + size, startY),
            'collides': False
        })

        particle3 = Particle({
            'vector': Vector2D(startX, startY + size),
            'collides': False
        })

        verlet.addParticle(particle1)
        verlet.addParticle(particle2)
        verlet.addParticle(particle3)

        edge1 = Constraint({
            'startParticle': particle1,
            'endParticle': particle2,
            'stiffness': 1,
            'collides': True,
            'objectID': objectIndex,
            'data': { 'drawn': True }
        })

        edge2 = Constraint({
            'startParticle': particle2,
            'endParticle': particle3,
            'stiffness': 1,
            'collides': True,
            'objectID': objectIndex,
            'data': { 'drawn': True }
        })

        edge3 = Constraint({
            'startParticle': particle3,
            'endParticle': particle1,
            'vstiffness': 1,
            'collides': True,
            'objectID': objectIndex,
            'data': { 'drawn': True }
        })

        verlet.addConstraint(edge1)
        verlet.addConstraint(edge2)
        verlet.addConstraint(edge3)

        verlet.addBody(Body({
            'edges': [
                edge1,
                edge2,
                edge3
            ],
            'collides': True
        }))

    @staticmethod
    def Cloth(verlet, startX, startY, links, linkLength, elasticity, tolerance, pinCorners):

        particleArray = {}
        xlinks = links * 2

        for i in range(0, xlinks):
            for o in range(0, links):
                pin = Vector2D(startX + (i * linkLength), startY + (o * linkLength)) if (o == 0 and (i == 0 or i == (xlinks - 1))) else None

                particle = Particle({
                    'vector': Vector2D(
                        startX + (i * linkLength),
                        startY + (o * linkLength)),
                    'pinnedTo': pin
                })

                particleArray[str(i) + "_" + str(o)] = particle

                verlet.addParticle(particle)

                if (i > 0):
                    verlet.addConstraint(
                        Constraint({
                            'startParticle': particle,
                            'endParticle': particleArray[str(i - 1) + "_" + str(o)],
                            'stiffness': elasticity,
                            'tolerance': tolerance,
                            'collides': True,
                            'objectID': 0,
                            'data': { 'drawn': True if (o % 4 == 0) or ((o == 0 or o == (links - 1))) else False }
                        }))

                if (o > 0):
                    verlet.addConstraint(
                        Constraint({
                            'startParticle': particle,
                            'endParticle': particleArray[str(i) + "_" + str((o - 1))],
                            'stiffness': elasticity,
                            'tolerance': tolerance,
                            'collides': True,
                            'objectID': 0,
                            'data': { 'drawn': True if  (i % 4 == 0) or ((i == 0 or i == (xlinks - 1))) else False }
                        }))