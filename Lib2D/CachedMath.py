import math  

global distanceCache
distanceCache = { }

global sineCache
sineCache = { }

def __init__(self):
    pass

def distance(x, y):
    global distanceCache

    if x in distanceCache:
        if y not in distanceCache[x]: 
            distanceCache[x].update({ y: math.sqrt(x * x + y * y) })
    else:
        distanceCache[x] = { y: math.sqrt(x * x + y * y) }

    # can we flip x and y?
    if y in distanceCache:
        if x not in distanceCache[y]: 
            distanceCache[y].update({ x: math.sqrt(y * y + x * x) })
    else:
        distanceCache[y] = { x: math.sqrt(y * y + x * x) }

    return distanceCache[x][y]

def sin(angle):
    global sineCache

    if angle not in sineCache:
        sineCache[angle] = math.sin(angle)

    return sineCache[angle]

def cos(angle):
    # offset cosine angle by 90 degrees ( 1.5708 radians ) to be a sine angle instead
    return sin(1.5708 - angle)
