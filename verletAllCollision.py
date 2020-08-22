import pygame
import random
import math
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 60
CANVAS_WIDTH = 1024
CANVAS_HEIGHT = 728
GRAVITY_DAMPENING = 0.001

##########################################################################

pygame.init()
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
done = False
clock = pygame.time.Clock()

verlet = Integration({
    'stageMinVect': Vector2D(10, 10),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 10, CANVAS_HEIGHT - 19),
    'gravity': Vector2D(0, 0.05)
})

objectSize = 60
objectID = 0

for x in range(0, 3):
    for y in range(0, 3):
        shape = 2  # random.randint(0, 3)

        if (shape == 0):
            Prefabs.Triangle(
                verlet,
                50 + x * (objectSize * 2),
                50 + y * (objectSize * 2),
                objectSize,
                1,
                objectID)

        elif (shape == 1):
            Prefabs.Box(
                verlet,
                50 + x * (objectSize * 2),
                50 + y * (objectSize * 2),
                objectSize,
                objectSize,
                random.randint(0, 360),
                True,
                0.35,
                objectID)

        else:
            particle1 = Particle({
                'vector': Vector2D(random.randint(0, CANVAS_WIDTH), random.randint(0, CANVAS_HEIGHT)),
                'radius': objectSize / 2,
                'collides': True,
                'objectID': objectID,
                'data': {'drawn': True}
            })

            verlet.addParticle(particle1)

        objectID += 1

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0, 0, 0))

    verlet.runTimeStep()
    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(
            screen,
            (0, 255, 0),
            (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y),
            (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    for particle in verlet.particles:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (int(particle.vector.x), int(particle.vector.y)),
            int(particle.radius or 1),
            1)

    pygame.display.flip()
    # clock.tick(FPS)
