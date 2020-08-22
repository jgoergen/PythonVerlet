import pygame
import random
import time
from math import floor
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
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
done = False
clock = pygame.time.Clock()

verlet = Integration({
    'iterations': 2,
    'stageMinVect': Vector2D(0, 0),
    'stageMaxVect': Vector2D(CANVAS_WIDTH, CANVAS_HEIGHT),
    'gravity': Vector2D(0, 0.05)
})

segmentLength = random.randint(10, 20) + 10
segments = random.randint(0, floor(40 / segmentLength)) + 10
# clock = pygame.time.Clock()

# drop a cloth
Prefabs.Cloth(
    verlet,
    ((CANVAS_WIDTH - 20) - ((segments * segmentLength) * 2)) / 2,
    ((CANVAS_HEIGHT - 20) - (segments * segmentLength)) / 2,
    segments,
    segmentLength,
    0.5,
    60,
    True)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # millis = int(round(time.time() * 1000))
    screen.fill((0, 0, 0))

    verlet.runTimeStep()
    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y),
            (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    # for particle in verlet.particles:
    #    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(particle.vector.x, particle.vector.y, 4, 4))

    pygame.display.flip()

    # print(int(round(time.time() * 1000)) - millis)

    # todo: change this to only wait if the desired time hasn't elapsed
    # clock.tick(FPS)
