import entity
import blocks
import objects
import os
import sys
import random


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
        for col in (cY - 5, cX + 5):
            fX.append(wX[col].icon)
        fX_joined = str(''.join(fX))
        print(fX_joined + "\n")

start_z = random.randint(1, (len(world) + 1))
start_x = random.randint(1, (len(world[1]) + 1))
start_y = random.randint(1, (len(world[1][1]) + 1))
player = entity.ROV(start_z, start_x, start_y, world)
world[player.z][player.x][player.y] = player
