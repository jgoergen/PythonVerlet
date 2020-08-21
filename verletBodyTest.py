from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Body

print('Libraries imported, running tests')

vect1 = Vector2D(10, 20)
vect2 = Vector2D(20, 20)
vect3 = Vector2D(20, 30)
vect4 = Vector2D(10, 30)
print('vect1 ' + vect1.toString())
print('vect2 ' + vect2.toString())
print('vect3 ' + vect2.toString())
print('vect4 ' + vect2.toString())

verlet = Integration({})

particle1 = Particle({'vector': vect1})
particle2 = Particle({'vector': vect2})
particle3 = Particle({'vector': vect3})
particle4 = Particle({'vector': vect4})

verlet.addParticle(particle1)
verlet.addParticle(particle2)
verlet.addParticle(particle3)
verlet.addParticle(particle4)

constraint1 = Constraint({
    'startParticle': particle1,
    'endParticle': particle2
})

constraint2 = Constraint({
    'startParticle': particle2,
    'endParticle': particle3
})

constraint3 = Constraint({
    'startParticle': particle3,
    'endParticle': particle4
})

constraint4 = Constraint({
    'startParticle': particle4,
    'endParticle': particle1
})

verlet.addConstraint(constraint1)
verlet.addConstraint(constraint2)
verlet.addConstraint(constraint3)
verlet.addConstraint(constraint4)

verlet.addBody(Body({
    'edges': [
        constraint1,
        constraint2,
        constraint3,
        constraint4
    ]}))

print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('particle 3: ' + verlet.particles[2].toString())
print('particle 4: ' + verlet.particles[3].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('particle 3: ' + verlet.particles[2].toString())
print('particle 4: ' + verlet.particles[3].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('particle 3: ' + verlet.particles[2].toString())
print('particle 4: ' + verlet.particles[3].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('particle 3: ' + verlet.particles[2].toString())
print('particle 4: ' + verlet.particles[3].toString())
print('')
