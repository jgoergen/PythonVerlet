import math
from Lib2D import Vector2D

class Body(object):

    def __init__(self, options):
        # initialize
        self.edges = options['edges'] if 'edges' in options else []
        self.data = options['data'] if 'data' in options else {}
        self.collides = options['collides'] if 'collides' in options else False
        self.mass = options['mass'] if 'mass' in options else 1

        # find unique vertexes
        self.uniqueVectors = []

        for i in range(0, len(self.edges)):
            if self.edges[i].ends.startParticle.vector not in self.uniqueVectors:
                self.uniqueVectors.append(self.edges[i].ends.startParticle.vector)

            if self.edges[i].ends.endParticle.vector not in self.uniqueVectors:
                self.uniqueVectors.append(self.edges[i].ends.endParticle.vector)

    def getCenter(self):
        centerX = 0
        centerY = 0

        for i in range(0, len(self.uniqueVectors)):
            centerX += self.uniqueVectors[i].x
            centerY += self.uniqueVectors[i].y

        return Vector2D(centerX / (len(self.uniqueVectors)), centerY / (len(self.uniqueVectors)))

    def getBounds(self):
        minX = 10000
        minY = 10000
        maxX = -10000
        maxY = -10000

        for i in range(0, len(self.uniqueVectors)):
            minX = min( minX, self.uniqueVectors[i].x, self.uniqueVectors[i].x)
            minY = min( minY, self.uniqueVectors[i].y, self.uniqueVectors[i].y)
            maxX = max( maxX, self.uniqueVectors[i].x, self.uniqueVectors[i].x)
            maxY = max( maxY, self.uniqueVectors[i].y, self.uniqueVectors[i].y)

        return [minX, minY, maxX, maxY]

    def projectToAxis(self, axisVect):
        dotP = axisVect.dotProduct(self.uniqueVectors[0])
        minVal = dotP 
        maxVal = dotP
        
        for i in range(0, len(self.uniqueVectors)):
            # Project the rest of the vertices onto the axis and extend 
            # the interval to the left/right if necessary
            dotP = axisVect.dotProduct(self.uniqueVectors[i])
            minVal = min(dotP, minVal)
            maxVal = max(dotP, maxVal)

        return [minVal, maxVal]

    def getCollision(self, body):
        # initialize the length of the collision vector to a relatively large value
        minDistance = 10000 
        collisionAxis = None
        collisionEdge = None
        collisionVector = None
        collisionEdgeBody = None
        primaryBody = None
        secondaryBody = None

        # just a fancy way of iterating through all of the edges of both bodies at once
        for i in range(0, len(self.edges) + len(body.edges)):
            edge = None

            if (i < len(self.edges)):
                edge = self.edges[i].ends
            else:
                edge = body.edges[i - len(self.edges)].ends

            # calculate the axis perpendicular to this edge and normalize it
            axisVect = Vector2D(
                edge.startParticle.vector.y - edge.endParticle.vector.y, 
                edge.endParticle.vector.x - edge.startParticle.vector.x) 

            axisVect.normalize()
            projection1 = self.projectToAxis(axisVect)
            projection2 = body.projectToAxis(axisVect)
            
            # calculate the distance between the two intervals - see below
            distance = projection2[0] - projection1[1] if projection1[0] < projection2[0] else projection1[0] - projection2[1]

            if (distance > 0):
                # if the intervals don't overlap, return, since there is no collision
                return None

            elif (abs(distance) < minDistance):
                # if they do and it's the shortest distance so far, save this info for response
                this = self
                minDistance = abs(distance)
                collisionAxis = axisVect
                collisionEdge = edge
                collisionEdgeBody = this if i < len(self.edges) else body

        primaryBody = this
        secondaryBody = body

        if (this == collisionEdgeBody):
            primaryBody = body
            secondaryBody = this

        # this is needed to make sure that the collision normal is pointing at B1
        sign = collisionAxis.dotProduct(
            secondaryBody
            .getCenter()
            .getSubtractedFromVector(
                primaryBody.getCenter())) > 0

        # remember that the line equation is N*( R - R0 ). We choose B2->Center 
        # as R0 the normal N is given by the collision normal
        if (sign == True):
            collisionAxis.reverse() # reverse the collision normal if it points away from B1

        smallestDistance = 10000

        for i in range(0, len(primaryBody.uniqueVectors)):
            # measure the distance of the vertex from the line using the line equation
            vertexDistance = collisionAxis.dotProduct(
                primaryBody.uniqueVectors[i].getSubtractedFromVector(
                    secondaryBody.getCenter()))
        
            # if the measured distance is smaller than the smallest distance reported 
            # so far, set the smallest distance and the collision vertex
            if (vertexDistance < smallestDistance):
                smallestDistance = vertexDistance
                collisionVector = primaryBody.uniqueVectors[i]

        return {
            'distance': minDistance,
            'collisionVector': collisionAxis,
            'edge': collisionEdge,
            'edgeBody': collisionEdgeBody,
            'vector': collisionVector,
            'vectorBody': primaryBody
        }

    def intervalDistance(self, minA, maxA, minB, maxB):
        if (minA < minB):
            return minB - maxA
        else:
            return minA - maxB