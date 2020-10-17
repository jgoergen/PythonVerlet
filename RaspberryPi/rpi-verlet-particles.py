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

for i in range(0, 40):
    verlet.addParticle(Particle({
        'vector': Vector2D(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)),
        'radius': 1 + random.randint(0, 3),
        'collides': True,
        'data': {
            'drawn': True,
            'color': graphics.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))}
    }))

skip = 0

while not done:

    if skip > 5:
        skip = 0
        mag = mpu9250.readMagnet()
        x = ((mag["z"] - 60) / 800) * -1
        y = ((mag["y"] + 27) / 800) * -1
        if (x is not 0 and y is not 0):
            verlet.gravity = Vector2D(x, y)
    else:
        skip += 1

    verlet.runTimeStep()
    matrix.Clear()

    for particle in verlet.particles:
        graphics.DrawCircle(matrix, int(particle.vector.x), int(
            particle.vector.y), particle.radius, particle.data['color'])

    time.sleep(0.015)
