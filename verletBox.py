import pygame
import random
import math
import time
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 60
CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 768
GRAVITY_DAMPENING = 0.001

##########################################################################

pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT), pygame.DOUBLEBUF)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
screen.set_alpha(None)
done = False
clock = pygame.time.Clock()

verlet = Integration({
    'stageMinVect': Vector2D(10, 10),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 10, CANVAS_HEIGHT - 10),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0

for x in range(0, 4):
    for y in range(0, 4):
        Prefabs.Box(
            verlet,
            random.randint(10, CANVAS_WIDTH - 10),
            random.randint(10, CANVAS_HEIGHT - 10),
            random.randint(100, 150),
            random.randint(100, 150),
            random.randint(0, 360),
            True,
            0.1,
            objectID)

        objectID += 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # millis = int(round(time.time() * 1000))
    screen.fill((0, 0, 0))

    verlet.runTimeStep()
    verlet.runTimeStep()
    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(screen, (0, 255, 0), (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y), (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    pygame.display.flip()

    # print(int(round(time.time() * 1000)) - millis)
    # todo: change this to only wait if the desired time hasn't elapsed
    # clock.tick(FPS)
