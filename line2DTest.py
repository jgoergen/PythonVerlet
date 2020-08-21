from Lib2D import Line2D
from Lib2D import Vector2D

print('Libraries imported, running tests')

vect1 = Vector2D(10, 20)
vect2 = Vector2D(20, 30)
line = Line2D(vect1, vect2)
print('Line ' + line.toString())
