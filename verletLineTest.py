from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint

print('Libraries imported, running tests')

vect1 = Vector2D(10, 20)
vect2 = Vector2D(20, 20)
print('vect1 ' + vect1.toString())
print('vect2 ' + vect2.toString())

verlet = Integration({})

particle1 = Particle({'vector': vect1})
particle2 = Particle({'vector': vect2})

verlet.addParticle(particle1)
verlet.addParticle(particle2)
verlet.addConstraint(Constraint({
    'startParticle': particle1,
    'endParticle': particle2
}))

print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('')
verlet.runTimeStep()
print('particle 1: ' + verlet.particles[0].toString())
print('particle 2: ' + verlet.particles[1].toString())
print('')
