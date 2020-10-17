#!/usr/bin/env python

# add the parent directory for importing
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import random
import math
import time
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import FaBo9Axis_MPU9250

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
CANVAS_WIDTH = 64
CANVAS_HEIGHT = 64
GRAVITY_DAMPENING = 0.001

##########################################################################

done = False

# init matrix

options = RGBMatrixOptions()
options.rows = CANVAS_WIDTH
options.cols = CANVAS_HEIGHT
matrix = RGBMatrix(options=options)

# init mpu9250
# https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/example/read9axis.py

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# init verlet

verlet = Integration({
    'iterations': 1,
    'stageMinVect': Vector2D(2, 2),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0
colors = []

for x in range(0, 4):
    for y in range(0, 2):
        Prefabs.Triangle(
            verlet,
            x * 20,
            y * 3,
            random.randint(8, 19),
            0.5,
            objectID)

        colors.append(graphics.Color(random.randint(0, 255),
                                     random.randint(0, 255), random.randint(0, 255)))
        objectID += 1

lineColor = graphics.Color(random.randint(
    0, 255), random.randint(0, 255), random.randint(0, 255))

skip = 0

while not done:

    if skip > 5:
        skip = 0
        mag = mpu9250.readMagnet()
        x = ((mag["z"] - 60) / 800) * -1
        y = ((mag["y"] + 27) / 800) * -1
        if (x is not 0 and y is not 0):
            verlet.gravity = Vector2D(x, y)
        # print x, y
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
