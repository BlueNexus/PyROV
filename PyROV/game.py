import entity
import blocks
import objects
import random


WORLD_Z = 20
WORLD_Y = 40
WORLD_X = 40
WORLD_ROCK_CHANCE = 15
WORLD_OBJECT_CHANCE = 1
PLAYER_VIEW_Y = 6
PLAYER_VIEW_X = 6

''' Everything is broken. Will fix soon
Todo: 
Move grabbing and dropping into world
Unbreak all the stuff
'''
player = None

class World:
    
    commands_dict = {"Q": "Move up", "W": "Move forward", "E": "Move down",
            "A": "Move left", "S": "Move back", "D": "Move right",
            "U": "Use item", "?": "Show commands", "I": "Show inventory",
            "G": "Grab", "F": "Drop"}
    commands_list = ["Q", "W", "E", "A", "S", "D", "U", "?", "I", "G", "F"]

    world = []

    def __init__(self, Z, Y, X, rock, obj, vY, vX):
        self.WORLD_Z = Z
        self.WORLD_Y = Y
        self.WORLD_X = X
        self.ROCK_CHANCE = rock
        self.OBJECT_CHANCE = obj
        self.VIEW_Y = vY
        self.VIEW_X = vX
        self.make_world(Z, Y, X)

    def make_world(self, z, y, x):
        working = []
        for plane in range(z):
            wZ = []
            for row in range(y):
                wY = []
                for col in range(x):
                    rand = random.randint(0, 100)
                    if rand > self.ROCK_CHANCE:
                        wX = blocks.Water(plane, col, row)
                    elif rand > self.OBJECT_CHANCE:
                        wX = blocks.Rock(plane, col, row)
                    else:
                        wX = objects.Object(plane, col, row)
                    wY.append(wX)
                wZ.append(wY)
            working.append(wZ)
        self.world = working
        print("Creating the player...")
        start_z = z / 2
        start_y = y / 2
        start_x = x / 2
        self.player = entity.ROV(start_z, start_y, start_x)
        self.world[self.player.z][self.player.y][self.player.x] = self.player
        print("Generation complete!")

    def print_world(self, thing):
        cur_Z = thing.z
        cur_Y = thing.y
        cur_X = thing.x
        working = self.world[cur_Z]
        # north_view_extent, east_view_extent, south_view_extent, west_view_extent = self.get_view_extents(thing, cur_Y, cur_X)
        # for row in range(cur_Y - north_view_extent, cur_Y + south_view_extent):
        for row in range(cur_Y - 5, cur_Y + 5):
            work_Y = working[row]
            final_Y = []
            # for col in range(cur_X - west_view_extent, cur_X + east_view_extent ):
            for col in range(cur_X - 5, cur_X + 5):
                final_Y.append(work_Y[col].icon)
            final_Y_joined = ' '.join(final_Y)
            print(final_Y_joined)

    def can_move(self, thing):
        moveable = []
        if self.world[thing.z][thing.y][thing.x + 1].passable:
            moveable.append(1)
        if self.world[thing.z][thing.y + 1][thing.x].passable:
            moveable.append(2)
        if self.world[thing.z][thing.y][thing.x - 1].passable:
            moveable.append(3)
        if self.world[thing.z][thing.y - 1][thing.x].passable:
            moveable.append(4)
        if self.world[thing.z + 1][thing.y][thing.x].passable:
            moveable.append(5)
        if self.world[thing.z - 1][thing.y][thing.x].passable:
            moveable.append(6)
        return moveable

    def replace_with_water(self, thing):
        self.world[thing.z][thing.y][thing.x] = blocks.Water(thing.z, thing.y, thing.x)

    def sync_coords(self, thing):
        self.world[thing.z][thing.y][thing.x] = thing

    def place_coords(self, thing, z, y, x):
        self.world[z][y][x] = thing

    def step(self, direc, thing):
        moveable = self.can_move(thing)
        if moveable and direc in moveable:
            self.replace_with_water(thing)
            if direc == 1:
                thing.y += 1
            elif direc == 2:
                thing.x += 1
            elif direc == 3:
                thing.y -= 1
            elif direc == 4:
                thing.x -= 1
            elif direc == 5:
                thing.z += 1
            elif direc == 6:
                thing.z -= 1
            self.sync_coords(thing)
        else:
            print("Thunk.")

    def show_commands(self):
        print(self.commands_dict)


    def handle_input(self, inp):
        if inp in self.commands_list:
            if inp == "Q":
                self.step(5, player)
            elif inp == "W":
                self.step(1, player)
            elif inp == "E":
                self.step(6, player)
            elif inp == "A":
                self.step(2, player)
            elif inp == "S":
                self.step(3, player)
            elif inp == "D":
                self.step(4, player)
            elif inp == "U":
                player.use()
            elif inp == "?":
                self.show_commands()
            elif inp == "I":
                player.show_inventory()
            elif inp == "G":
                available = self.get_adjacent(player)
                print("Adjacent items: ")
                for item in available:
                    print(item.name)
                chose = str(raw_input("Choose which item to grab > "))
                valid = False
                for item in available:
                    if chose == item.name:
                        player.grab(item, self)
                        valid = True
                        break
                if not valid:
                    print("Invalid item!")
            elif inp == "F":
                    player.drop(self)
        else:
            print("Invalid command. Enter '?' for a list of commands.")

def options_get_value(choice):
    return int(raw_input("Enter a value for " + str(editing) + " > "))

print("PyROV: v0.14.0-Alpha")
print("-" * 10)

print("1. Start")
print("2. Options")

while True:
    choice = str(raw_input("Enter your choice (Start/Options) > ")).title()
    if choice == "Start":
        globe = World(WORLD_Z, WORLD_Y, WORLD_X, WORLD_ROCK_CHANCE,
                        WORLD_OBJECT_CHANCE, PLAYER_VIEW_Y,
                        PLAYER_VIEW_X)
        global player
        player = globe.player
        while True:
            globe.print_world(player)
            print("Power remaining: " + str(player.cell.power))
            globe.handle_input(str(raw_input(">> ")).title())

    elif choice == "Options":
        global WORLD_Z
        global WORLD_Y
        global WORLD_X
        global WORLD_ROCK_CHANCE
        global WORLD_OBJECT_CHANCE
        global PLAYER_VIEW_Y
        global PLAYER_VIEW_X
        print("Z-levels: " + str(WORLD_Z))
        print("Y-levels: " + str(WORLD_Y))
        print("X-levels: " + str(WORLD_X))
        print("Worldgen rock chance: " + str(WORLD_ROCK_CHANCE))
        print("Worldgen object chance: " + str(WORLD_OBJECT_CHANCE))
        print("Player Y view size: " + str(PLAYER_VIEW_Y))
        print("Player X view size: " + str(PLAYER_VIEW_X))
        editing = str(raw_input("Choose which setting to change, or enter 'Exit' to go back to the menu > ")).title()
        try:
            if editing == "Z-Levels":
                WORLD_Z = options_get_value(editing)
            elif editing == "Y-Levels":
                WORLD_Y = options_get_value(editing)
            elif editing == "X-Levels":
                WORLD_X = options_get_value(editing)
            elif editing == "Worldgen Rock Chance":
                WORLD_ROCK_CHANCE = options_get_value(editing)
            elif editing == "Worldgen Object Chance":
                WORLD_OBJECT_CHANCE = options_get_value(editing)
            elif editing == "Player Y View Size":
                PLAYER_VIEW_Y = options_get_value(editing)
            elif editing == "Player X View Size":
                PLAYER_VIEW_X = options_get_value(editing)
        except:
            pass



'''
    def get_view_extents(self, thing, y, x):
        east = min(x + self.VIEW_X, len(self.world[thing.z][thing.y]) - 1)
        west = max(x - self.VIEW_X, 0)
        south = min(y + self.VIEW_Y, len(self.world[thing.z]) - 1)
        north = max(y - self.VIEW_Y, 0)
        return north, east, south, west
'''
