import entity
import blocks
import objects
import os
import sys
import random

# CONFIG
WORLD_Z = 10
WORLD_X = 20
WORLD_Y = 20
# END CONFIG

world = []

def make_world(z, x, y):
    working = []
    for plane in range(z):
        wZ = []
        for row in range(x):
            wX = []
            for col in range(y):
                if random.randint(0, 100) > 10:
                    wY = blocks.Water()
                else:
                    wY = blocks.Rock()
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

make_world(WORLD_Z, WORLD_X, WORLD_Y)
start_z = random.randint(0, (len(world) + 1))
start_x = random.randint(0, (len(world[1]) + 1))
start_y = random.randint(0, (len(world[1][1]) + 1))
player = entity.ROV(start_z, start_x, start_y, world)
world[player.z][player.x][player.y] = player


