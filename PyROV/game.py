import entity
import enviro
import objects
import setup
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
                wY = " "
                wX.append(wY)
            wZ.append(wX)
        working.append(wZ)
    global world
    world = working

def print_world(current, cX, cY):
    global world
    working = world[current]
    for row in range(cX - 5, cX + 5):
        wX = working[row]
        fX = []
        for col in wX:
            fX.append(col.icon)
        fX_joined = str(''.join(fX))
        print(fX_joined + "\n")
        
