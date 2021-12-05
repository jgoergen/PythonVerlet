import pygame
import random
import math
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 60
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
GRAVITY_DAMPENING = 0.001

##########################################################################

pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
done = False
clock = pygame.time.Clock()

verlet = Integration({
    'stageMinVect': Vector2D(0, 0),
    'stageMaxVect': Vector2D(CANVAS_WIDTH, CANVAS_HEIGHT),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0

for x in range(0, 5):
    for y in range(0, 5):
        triangleSize = random.randint(50, 100)
        Prefabs.Triangle(
            verlet,
            random.randint(0, CANVAS_WIDTH),
            random.randint(0, CANVAS_HEIGHT),
            triangleSize,
            1,
            objectID)

        objectID += 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    verlet.runTimeStep()
    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(screen, (0, 255, 0), (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y),
                         (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    pygame.display.flip()
    # clock.tick(FPS)
