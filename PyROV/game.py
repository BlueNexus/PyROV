import rov
import objects
import os
import sys


world = []

def make_world(z, x, y):
    working = []
    for plane in range(z):
        wZ = []
        for row in range(x):
            wX = []
            for col in range(y):
                wY = []
                wX.append(wY)
            wZ.append(wX)
        working.append(wZ)
    global world
    world = working
