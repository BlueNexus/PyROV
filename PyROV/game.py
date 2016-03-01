import entity
import blocks
import objects
import os
import sys
import random
import readchar

# CONFIG
WORLD_Z = 10
WORLD_X = 20
WORLD_Y = 20
# END CONFIG

commands_dict = {"Q": "Move up", "W": "Move forward", "E": "Move down",
            "A": "Move left", "S": "Move back", "D": "Move right",
            "?": "Show commands", "I": "Show inventory", "G": "Grab",
            "F": "Drop"}
commands_list = ["Q", "W", "E", "A", "S", "D", "?", "I", "G", "F"]
world = []
clear = lambda: os.system('cls')

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

def print_world(cZ, cX, cY):
    global world
    working = world[cZ]
    for row in range(cX - 5, cX + 5):
        wX = working[row]
        fX = []
        for col in (cY - 5, cX + 5):
            fX.append(wX[col].icon)
        fX_joined = str(''.join(fX))
        print(fX_joined + "\n")

def show_commands():
    global commands_dict
    print(commands_dict)

def handle_input(inp):
    global commands_list
    global world
    if inp in commands_list:
        if inp == "Q":
            player.move(5, world)
        elif inp == "W":
            player.move(1, world)
        elif inp == "E":
            player.move(6, world)
        elif inp == "A":
            player.move(4, world)
        elif inp == "S":
            player.move(3, world)
        elif inp == "D":
            player.move(2, world)
        elif inp == "?":
            show_commands()
        elif inp == "I":
            player.show_inventory()
        elif imp == "G":
            available = player.get_adjacent_items(world)
            print("Adjacent items: ")
            for item in available:
                print(item.name + "\n")
            chose = str(raw_input("Choose which item to grab: "))
            valid = False
            for item in available:
                if chose == item.name:
                    player.grab(item, world)
                    valid = True
                    break
            if not valid:
                print("Invalid item!")
        elif imp == "F":
            player.drop(world)
    else:
        print("Invalid command. Enter '?' for a list of commands.")

# World generation
make_world(WORLD_Z, WORLD_X, WORLD_Y)
start_z = random.randint(0, (len(world) + 1))
start_x = random.randint(0, (len(world[1]) + 1))
start_y = random.randint(0, (len(world[1][1]) + 1))
player = entity.ROV(start_z, start_x, start_y, world)
world[player.z][player.x][player.y] = player

while True:
    clear()
    print_world(player.z, player.x, player.y)
    handle_input(readchar.readchar())

