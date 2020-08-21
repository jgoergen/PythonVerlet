import random, math, time
from Lib2D import Vector2D
from VerletIntegration import Integration, Particle, Constraint, Prefabs
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import FaBo9Axis_MPU9250

# Settings #############################################################

# put any adjustable settings here that would be interesting to tinker with.

FPS = 30
CANVAS_WIDTH = 64
CANVAS_HEIGHT = 32
GRAVITY_DAMPENING = 0.001

##########################################################################

done = False

# init matrix

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
# options.brightness = self.args.led_brightness
matrix = RGBMatrix(options = options)

# init mpu9250
# https://github.com/FaBoPlatform/FaBo9AXIS-MPU9250-Python/blob/master/example/read9axis.py

mpu9250 = FaBo9Axis_MPU9250.MPU9250()

# init verlet

verlet = Integration({
    'iterations': 2,
    'stageMinVect': Vector2D(2, 2),
    'stageMaxVect': Vector2D(CANVAS_WIDTH - 2, CANVAS_HEIGHT - 2),
    'gravity': Vector2D(0, 0.05)
})

objectID = 0
colors = []

for x in range(0, 4):
    for y in range(0, 2):
        Prefabs.Triangle(
            verlet,
            x * 20,
            y * 3,
            random.randint(8, 19), 
            0.5,
            objectID)

        colors.append(graphics.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        objectID += 1

lineColor = graphics.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

highestMX = 0
lowestMX = 0
highestMY = 0
lowestMY = 0

def testMPU():
    # accel = mpu9250.readAccel()
    # print " ax = " , ( accel['x'] )
    # print " ay = " , ( accel['y'] )
    # print " az = " , ( accel['z'] )

    # gyro = mpu9250.readGyro()
    # print " gx = " , ( gyro['x'] )
    # print " gy = " , ( gyro['y'] )
    # print " gz = " , ( gyro['z'] )

    mag = mpu9250.readMagnet()

    if mag['x'] > highestMX:
        highestMX = mag['x']

    if mag['x'] < lowestMX:
        lowestMX = mag['x']

    if mag['y'] > highestMY:
        highestMY = mag['y']

    if mag['y'] < lowestMY:
        lowestMY = mag['y']

    #print " X: " , mag['x'], ": ", lowestMX, " - ", highestMX
    #print " my = " , mag['y'], ": ", lowestMY, " - ", highestMY
    #print " mz = " , ( mag['z'] )
    #print('')

skip = 0

while not done:

    if skip > 10:
        skip = 0
        mag = mpu9250.readMagnet()
        x = ((mag['x']) / 100) * -1
        y = ((mag['y']) / 100) * -1
        verlet.gravity = Vector2D(x, y)
        # print x, y
    else:
        skip += 1
    
    verlet.runTimeStep()
    matrix.Clear()

    for constraint in verlet.constraints:
        if ('drawn' in constraint.data and constraint.data['drawn'] == True):
            graphics.DrawLine(
                matrix, 
                constraint.ends.startParticle.vector.x, 
                constraint.ends.startParticle.vector.y, 
                constraint.ends.endParticle.vector.x, 
                constraint.ends.endParticle.vector.y, 
                colors[constraint.objectID])

    time.sleep(0.015)