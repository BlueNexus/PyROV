import entity
import blocks
import objects
import random

# CONFIG
WORLD_Z = 20
WORLD_X = 40
WORLD_Y = 40
WORLDGEN_ROCK_CHANCE = 15
WORLDGEN_OBJECT_CHANCE = 1
PLAYER_VIEW_X = 6
PLAYER_VIEW_Y = 6
# END CONFIG

commands_dict = {"Q": "Move up", "W": "Move forward", "E": "Move down",
            "A": "Move left", "S": "Move back", "D": "Move right",
            "U": "Use item", "?": "Show commands", "I": "Show inventory",
            "G": "Grab", "F": "Drop"}
commands_list = ["Q", "W", "E", "A", "S", "D", "U", "?", "I", "G", "F"]
world = []
player = None

def make_world(z, x, y):
    print("Generating world...")
    working = []
    for plane in range(z):
        print("Generating Z-level " + str(plane) + " of " + str(z))
        wZ = []
        for row in range(x):
            wX = []
            for col in range(y):
                rand = random.randint(0, 100)
                if rand > WORLDGEN_ROCK_CHANCE:
                    wY = blocks.Water(plane, row, col)
                elif rand > WORLDGEN_OBJECT_CHANCE:
                    wY = blocks.Rock(plane, row, col)
                else:
                    wY = objects.Object(plane, row, col)
                wX.append(wY)
            wZ.append(wX)
        working.append(wZ)
    global world
    global player
    world = working
    print("Creating the player...")
    start_z = z / 2
    start_x = x / 2
    start_y = y / 2
    player = entity.ROV(start_z, start_x, start_y)
    world[player.z][player.x][player.y] = player
    print("Generation complete!")

def print_world(cZ, cX, cY):
    global world
    working = world[cZ]
    for row in range(cX - PLAYER_VIEW_X, cX + PLAYER_VIEW_X):
        wX = working[row]
        fX = []
        for col in range(cY - PLAYER_VIEW_Y, cY + PLAYER_VIEW_Y):
            fX.append(wX[col].icon)
        fX_joined = ' '.join(fX)
        print(fX_joined)

def show_commands():
    global commands_dict
    print(commands_dict)


def handle_input(inp):
    global world
    if inp in commands_list:
        if inp == "Q":
            player.move(5, world)
        elif inp == "W":
            player.move(4, world)
        elif inp == "E":
            player.move(6, world)
        elif inp == "A":
            player.move(3, world)
        elif inp == "S":
            player.move(2, world)
        elif inp == "D":
            player.move(1, world)
        elif inp == "U":
            player.use()
        elif inp == "?":
            show_commands()
        elif inp == "I":
            player.show_inventory()
        elif inp == "G":
            available = player.get_adjacent_items(world)
            print("Adjacent items: ")
            for item in available:
                print(item.name)
            chose = str(raw_input("Choose which item to grab > "))
            valid = False
            for item in available:
                if chose == item.name:
                    player.grab(item, world)
                    valid = True
                    break
            if not valid:
                print("Invalid item!")
        elif inp == "F":
            player.drop(world)
    else:
        print("Invalid command. Enter '?' for a list of commands.")

def options_get_value(choice):
    return int(raw_input("Enter a value for " + str(editing) + " > "))

print("PyROV: v0.14.0-Alpha")
print("-" * 10)

while True:
    print("1. Start")
    print("2. Options")
    choice = str(raw_input("Enter your choice (Start/Options) > ")).title()
    if choice == "Start":
        make_world(WORLD_Z, WORLD_X, WORLD_Y)
        while True:
            print_world(player.z, player.x, player.y)
            print("Power remaining: " + str(player.cell.power))
            handle_input(str(raw_input(">> ")).title())

    elif choice == "Options":
        global WORLD_Z
        global WORLD_X
        global WORLD_Y
        global WORLDGEN_ROCK_CHANCE
        global WORLDGEN_OBJECT_CHANCE
        global PLAYER_VIEW_X
        global PLAYER_VIEW_Y
        print("Z-levels: " + str(WORLD_Z))
        print("X-levels: " + str(WORLD_X))
        print("Y-levels: " + str(WORLD_Y))
        print("Worldgen rock chance: " + str(WORLDGEN_ROCK_CHANCE))
        print("Worldgen object chance: " + str(WORLDGEN_OBJECT_CHANCE))
        print("Player X view size: " + str(PLAYER_VIEW_X))
        print("Player Y view size: " + str(PLAYER_VIEW_Y))
        editing = str(raw_input("Choose which setting to change, or enter 'Exit' to go back to the menu > ")).title()
        try:
            if editing == "Z-Levels":
                WORLD_Z = options_get_value(editing)
            elif editing == "X-Levels":
                WORLD_X = options_get_value(editing)
            elif editing == "Y-Levels":
                WORLD_Y = options_get_value(editing)
            elif editing == "Worldgen Rock Chance":
                WORLDGEN_ROCK_CHANCE = options_get_value(editing)
            elif editing == "Worldgen Object Chance":
                WORLDGEN_OBJECT_CHANCE = options_get_value(editing)
            elif editing == "Player X View Size":
                PLAYER_VIEW_X = options_get_value(editing)
            elif editing == "Player Y View Size":
                PLAYER_VIEW_Y = options_get_value(editing)
            else:
                pass
        except:
            pass

