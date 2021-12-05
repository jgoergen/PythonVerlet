import pygame
import random
import math
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
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

for i in range(0, 100):
    verlet.addParticle(Particle({
        'vector': Vector2D(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)),
        'radius': 5 + random.randint(0, 15),
        'collides': True,
        'data': {'drawn': True}
    }))

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    verlet.runTimeStep()
    verlet.runTimeStep()

    for particle in verlet.particles:
        pygame.draw.circle(screen, (0, 255, 0), (int(
            particle.vector.x), int(particle.vector.y)), particle.radius, 1)

    pygame.display.flip()
    # clock.tick(FPS)
