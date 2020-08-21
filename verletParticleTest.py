from Lib2D import Vector2D
from VerletIntegration import Integration, Particle

print('Libraries imported, running tests')

vect1 = Vector2D(10, 20)
print('vect1 ' + vect1.toString())

verlet = Integration({})
verlet.addParticle(Particle({'vector': vect1}))

print(verlet.particles[0].toString())
print('')
verlet.runTimeStep()
print(verlet.particles[0].toString())
print('')
verlet.runTimeStep()
print(verlet.particles[0].toString())
print('')
verlet.runTimeStep()
print(verlet.particles[0].toString())
print('')
