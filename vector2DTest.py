from Lib2D import Vector2D

print('Library imported, running tests')

vect = Vector2D(10, 20)
print('vect x: ' + str(vect.x) + ' y: ' + str(vect.y))

print('reversing')
vect2 = vect.copy()
vect.reverse()
print('vect x: ' + str(vect.x) + ' y: ' + str(vect.y))
print('magnitude ' + str(vect.magnitude()) + ', ' + str(vect2.magnitude()))
print('')

vect3 = vect.getSubtractedFromScalar(5)
vect4 = vect.getSubtractedFromVector(vect2)
print('vect3 x: ' + str(vect3.x) + ' y: ' + str(vect3.y))
print('vect4 x: ' + str(vect4.x) + ' y: ' + str(vect4.y))
print('')

vect5 = vect.getAddedToVector(vect2)
print('vect5 x: ' + str(vect5.x) + ' y: ' + str(vect5.y))
print('')

vect5.addToVector(Vector2D(10, 0))
print('vect5 x: ' + str(vect5.x) + ' y: ' + str(vect5.y))
print('')

vect5.addToVector(Vector2D(0, 10))
print('vect5 x: ' + str(vect5.x) + ' y: ' + str(vect5.y))
print('')

vect6 = Vector2D(-6, 8)
vect7 = Vector2D(5, 12)
dot = vect6.dotProduct(vect7)
print('dot ' + str(dot))
print('')