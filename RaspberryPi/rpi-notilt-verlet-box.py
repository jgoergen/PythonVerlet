#!/usr/bin/env python

# add the parent directory for importing
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
from VerletIntegration import Integration, Particle, Constraint, Prefabs
from Lib2D import Vector2D
import time
import math
import random


# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
CANVAS_WIDTH = 32
CANVAS_HEIGHT = 64
GRAVITY_DAMPENING = 0.001

##########################################################################

done = False

# init matrix

options = RGBMatrixOptions()
options.rows = CANVAS_WIDTH
options.cols = CANVAS_HEIGHT
matrix = RGBMatrix(options=options)

# init verlet

verlet = Integration({
    'iterations': 1,
    'stageMinVect': Vector2D(2, 2),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0
colors = []

for x in range(0, 3):
    for y in range(0, 3):
        Prefabs.Box(
            verlet,
            x * 10,
            y * 10,
            random.randint(5, 15),
            random.randint(5, 15),
            random.randint(0, 360),
            True,
            0.65,
            objectID)

        colors.append(
            graphics.Color(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)))

        objectID += 1

lineColor = graphics.Color(random.randint(
    0, 255), random.randint(0, 255), random.randint(0, 255))

skip = 0

while not done:

    if skip > 5:
        skip = 0
        # x = ((mag["z"] - 60) / 800) * -1
        # y = ((mag["y"] + 27) / 800) * -1
        # if (x is not 0 and y is not 0):
        #     verlet.gravity = Vector2D(x, y)
    else:
        skip += 1

    verlet.runTimeStep()
    matrix.Clear()

    for constraint in verlet.constraints:
        if ('drawn' in constraint.data and constraint.data['drawn'] == True):
            graphics.DrawLine(
                matrix,
                constraint.ends.startParticle.vector.x,
                constraint.ends.startParticle.vector.y,
                constraint.ends.endParticle.vector.x,
                constraint.ends.endParticle.vector.y,
                colors[constraint.objectID])

    time.sleep(0.015)
