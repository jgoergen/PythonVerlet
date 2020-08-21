import pygame
import random, math
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 500
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

segmentLength = random.randint(0, 10) + 3
segments = random.randint(0, math.floor(80 / segmentLength)) + 20

# drop a cloth
Prefabs.Cloth(
    verlet,
    ((CANVAS_WIDTH - 20) - ((segments * segmentLength) * 2)) / 2,
    ((CANVAS_HEIGHT - 20) - (segments * segmentLength)) / 2,
    segments, 
    segmentLength, 
    1, 
    60,
    True)

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0))

    verlet.runTimeStep()

    for constraint in verlet.constraints:
        pygame.draw.line(screen, (0,255,0), (constraint.ends.startParticle.vector.x, constraint.ends.startParticle.vector.y), (constraint.ends.endParticle.vector.x, constraint.ends.endParticle.vector.y))

    #for particle in verlet.particles:
    #    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(particle.vector.x, particle.vector.y, 4, 4))

    pygame.display.flip()
    clock.tick(FPS)
