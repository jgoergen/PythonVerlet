import pygame
import random
import time
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 768
GRAVITY_DAMPENING = 0.001

##########################################################################

pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
done = False
clock = pygame.time.Clock()

verlet = Integration({
    'iterations': 1,
    'stageMinVect': Vector2D(0, 0),
    'stageMaxVect': Vector2D(CANVAS_WIDTH, CANVAS_HEIGHT),
    'gravity': Vector2D(0, 0.05)
})

for i in range(0, 200):
    Prefabs.Rope(verlet,
                 375 + (random.randint(0, CANVAS_WIDTH - 750)),
                 225 + (random.randint(0, CANVAS_HEIGHT - 450)),
                 random.randint(0, 25) + 5,
                 random.randint(0, 3) + 4,
                 1,
                 True)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # millis = int(round(time.time() * 1000))

    screen.fill((0, 0, 0))

    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(screen, (0, 255, 0), (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y), (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    pygame.display.flip()

    # print(int(round(time.time() * 1000)) - millis)

    clock.tick(FPS)
