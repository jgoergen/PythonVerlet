# PythonVerlet
A Python implementation of the Verlet algorithm based on my JavaScript implementation.

## really helpful material when optimizing this for Python 3
* https://shocksolution.com/2009/01/09/optimizing-python-code-for-fast-math/

## todo
python verletAllCollision.py
    only balls are enabled and their collision is way too strong when they're very close. I'm using cmath in the collisionfunctions.Circle collision which appears to be slow? but math.sqrt doesn't accept negative numbers so i had to. there is another version of the circle on line collision i was trying but i'm not sure if it's messed up or something else is.