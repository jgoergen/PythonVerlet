# Python Verlet Algorythm
My attempt at the popular ( velocity-less ) Verlet Algorythm written in Python. This is based on my JavaSscript implementation which can be found [here](https://github.com/jgoergen/VerletAlgorythm).

#### Basically all of this math has been pulled together from research online. I am definetley not good enough at math to come up with most of these equations myself, so the truly heavy lifting has been lifted / adapted from resources found all over the internet.

# **This is a work in progress!**

Really, this is mostly a passion project for me. There are many other libraries that would be faster and easier to use that exist, ofcourse. I mostly just want to learn the math, porting between languages, and I like to make my own libraries for fun / experience / learning.  

The Javascript implimentation is my main focus at the moment, c#, python and C will come as I get time, but they will be based on the initial and proven Javascript implimentation.

## Helpful material when optimizing this for Python 3
* https://shocksolution.com/2009/01/09/optimizing-python-code-for-fast-math/


## Verlet Integration Todo ( in no particular order )
**ALOT**
1. Everything needs to honor a time delta.
2. There should be a mode that scales the iterations depending on how bad the time deltas get.
3. Add attractive and repulsive forces
4. Add collision response callbacks ( which include collision information )
5. look into adding quadtree or binary space partitioning to speed everything up
    * https://en.wikipedia.org/wiki/Binary_space_partitioning
    * https://en.wikipedia.org/wiki/Quadtree
    * maybe use this? http://gameprogrammingpatterns.com/spatial-partition.html

## Code Todo ( in no particular order )
**ALOT**
1. All the classes could be re-written and improved.
2. OPTIMIZE OPTIMIZE OPTIMIZE.
3. Any cheaper / less accurate ways to calculate things for speed? These make nice options.
    * https://stackoverflow.com/questions/21010586/normalizing-spatial-vectors-without-square-root
4. Some way to easily test all the math in the classes would be helpful.
5. Mark objects (particles / constraints / bodies) as dirty / clean on update cycles so if they haven't moved then they don't need to be reconsidered this pass
6. Add more prefabs and add more settings to each prefab so everything can be adjusted

## Things to read and draw inspiration from
1. https://gamedevelopment.tutsplus.com/tutorials/how-to-create-a-custom-2d-physics-engine-oriented-rigid-bodies--gamedev-8032
2. https://github.com/tutsplus/ImpulseEngine/blob/master/Collision.cpp
3. https://gamedev.stackexchange.com/questions/74858/how-can-i-improve-my-collision-detections-performance
4. https://code.google.com/archive/p/box2d/downloads
5. https://stackoverflow.com/questions/345838/ball-to-ball-collision-detection-and-handling