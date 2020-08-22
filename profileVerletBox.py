import pygame
import random
import math
import time
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs
import cProfile
import pstats

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
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
    'iterations': 3,
    'stageMinVect': Vector2D(10, 10),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 10, CANVAS_HEIGHT - 10),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0

for x in range(0, 4):
    for y in range(0, 4):
        Prefabs.Box(
            verlet,
            50 + x * 70,  # Math.random() * (CANVAS_WIDTH - 400) + 200,
            50 + y * 60,  # Math.random() * (CANVAS_HEIGHT - 400) + 200,
            random.randint(30, 80),
            random.randint(30, 80),
            random.randint(0, 360),
            True,
            1,
            objectID)

        objectID += 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    millis = int(round(time.time() * 1000))

    screen.fill((0, 0, 0))

    profile = cProfile.Profile()
    profile.enable()
    profile.runcall(verlet.runTimeStep, "verlet")
    done = True

    for constraint in verlet.constraints:
        pygame.draw.line(screen, (0, 255, 0), (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y), (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    pygame.display.flip()

    print(int(round(time.time() * 1000)) - millis)

    clock.tick(FPS)

    ps = pstats.Stats(profile)
    ps.print_stats()
