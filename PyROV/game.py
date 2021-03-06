import entity
import blocks
import objects
import random
import os
import logging


WORLD_Z = 10
WORLD_Y = 160
WORLD_X = 160
PLAYER_VIEW_Y = 12
PLAYER_VIEW_X = 12
DEBUG = True
player = None

logging.basicConfig(level=logging.ERROR, filename='log/errorlog.log')

class World:
    
    commands_dict = {"Q": "Move up", "W": "Move forward", "E": "Move down",
            "A": "Move left", "S": "Move back", "D": "Move right",
            "U": "Use item", "?": "Show commands", "I": "Show inventory",
            "G": "Grab", "F": "Drop"}
    commands_list = ["Q", "W", "E", "A", "S", "D", "U", "?", "I", "G", "F"]

    def __init__(self, Z, Y, X, vY, vX, de):
        self.WORLD_Z = Z
        self.WORLD_Y = Y
        self.WORLD_X = X
        self.VIEW_Y = vY
        self.VIEW_X = vX
        self.DEBUG = de
        self.make_world(Z, Y, X)

    def make_world(self, z, y, x):
        working = self.generate_world(z, y, x)
        self.world = working
        print("Creating the player...")
        start_z = int(z / 2)
        start_y = 0
        start_x = 0
        self.player = entity.ROV(start_z, start_y, start_x)
        self.world[self.player.z][self.player.y][self.player.x] = self.player
        if self.DEBUG:
            self.debug_world_sync()
        print("Generation complete!")

    def generate_world(self, z, y, x):
        world = self.worldgen_stage_1(z, y, x)
        world = self.worldgen_stage_2(world)
        world = self.worldgen_stage_3(world)
        return world

    def worldgen_stage_1(self, z, y, x):
        print("Worldgen: Generating base world")
        work = []
        for plane in range(z):
            wZ = []
            for row in range(y):
                wY = []
                for col in range(x):
                    if plane == 0:
                        wX = blocks.Rock(plane, row, col)
                    else:
                        wX = blocks.Water(plane, row, col)
                    wY.append(wX)
                wZ.append(wY)
            work.append(wZ)
        print("Worldgen: Base world generation complete")
        return work

    def worldgen_stage_2(self, base):
        print("Worldgen: Generating terrain")
        for plane_no, plane in enumerate(base):
            for row_no, row in enumerate(plane):
                for col_no, col in enumerate(row):
                    if plane_no != 0:
                        rand = random.randint(0, 100)
                        if self.can_support(plane_no, row_no, col_no, base):
                            if rand > 10:
                                self.gen_create(blocks.Rock, base, plane_no, row_no, col_no)
        print("Worldgen: Terrain generation complete")
        return base

    def worldgen_stage_3(self, base):
        print("Worldgen: Placing items")
        for plane_no, plane in enumerate(base):
            for row_no, row in enumerate(plane):
                for col_no, col in enumerate(row):
                    rand = random.randint(0, 100)
                    if isinstance(base[plane_no - 1][row_no][col_no], blocks.Rock) and rand > 95:
                        self.gen_create(objects.Cell, base, plane_no, row_no, col_no)
        print("Worldgen: Items placed")
        return base

    def create(self, thing, z, y, x):
        item = thing(z, y, x)
        self.sync_coords(thing)

    def gen_create(self, thing, base, z, y, x):
        item = thing(z, y, x)
        base[z][y][x] = item

    def can_support(self, plane_no, row_no, col_no, base):
        checking = base[plane_no - 1][row_no][col_no]
        if isinstance(checking, blocks.Rock):
            try:
                to_check = []
                if row_no != 0:
                    to_check.append(base[plane_no - 1][row_no - 1][col_no])
                if row_no != (self.WORLD_Y * 2):
                    to_check.append(base[plane_no - 1][row_no + 1][col_no])
                if col_no != 0:
                    to_check.append(base[plane_no - 1][row_no][col_no - 1])
                if col_no != (self.WORLD_X * 2):
                    to_check.append(base[plane_no - 1][row_no][col_no + 1])
                valid = True
                for block in to_check:
                    if not isinstance(block, blocks.Rock):
                        valid = False
            except:
                valid = False
            return valid
        else:
            return False

    def debug_world_sync(self):
        for plane in self.world:
            for col in plane:
                for row in col:
                    self.sync_coords(row)

    def get_view_extents(self, thing):
        east = min(self.VIEW_X + 1, len(self.world[thing.z][thing.y]) - thing.x)
        west = min(self.VIEW_X, len(self.world[thing.z][thing.y]) + thing.x)
        south = min(self.VIEW_Y + 1, len(self.world[thing.z]) - thing.y)
        north = min(self.VIEW_Y, len(self.world[thing.z]) + thing.y)
        return north, east, south, west

    def print_world(self, thing):
        cur_Z = thing.z
        cur_Y = thing.y
        cur_X = thing.x
        working = self.world[cur_Z]
        north_view_extent, east_view_extent, south_view_extent, west_view_extent = self.get_view_extents(thing)
        for row in range(cur_Y - north_view_extent, cur_Y + south_view_extent):
            work_Y = working[row]
            final_Y = []
            for col in range(cur_X - west_view_extent, cur_X + east_view_extent ):
                final_Y.append(str(work_Y[col]))
            final_Y_joined = ' '.join(final_Y)
            print(final_Y_joined)

    def can_move(self, thing):
        moveable = []
        try:
            if self.world[thing.z][thing.y - 1][thing.x].passable:
                moveable.append(1)
        except:
            pass
        try:
            if self.world[thing.z][thing.y][thing.x - 1].passable:
                moveable.append(2)
        except:
            pass
        try:
            if self.world[thing.z][thing.y + 1][thing.x].passable:
                moveable.append(3)
        except:
            pass
        try:
            if self.world[thing.z][thing.y][thing.x + 1].passable:
                moveable.append(4)
        except:
            pass
        try:
            if self.world[thing.z + 1][thing.y][thing.x].passable:
                moveable.append(5)
        except:
            pass
        try:
            if self.world[thing.z - 1][thing.y][thing.x].passable:
                moveable.append(6)
        except:
            pass
        return moveable

    def get_adjacent(self, thing):
        adjacent = []
        if self.world[thing.z][thing.y - 1][thing.x].can_grab:
            adjacent.append(self.world[thing.z][thing.y - 1][thing.x])
        if self.world[thing.z][thing.y][thing.x - 1].can_grab:
            adjacent.append(self.world[thing.z][thing.y][thing.x - 1])
        if self.world[thing.z][thing.y + 1][thing.x].can_grab:
            adjacent.append(self.world[thing.z][thing.y + 1][thing.x])
        if self.world[thing.z][thing.y][thing.x + 1].can_grab:
            adjacent.append(self.world[thing.z][thing.y][thing.x + 1])
        return adjacent

    def replace_with_water(self, thing):
        self.world[thing.z][thing.y][thing.x] = blocks.Water(thing.z, thing.y, thing.x)

    def sync_coords(self, thing):
        self.world[thing.z][thing.y][thing.x] = thing

    def match_coords(self, child, parent):
        self.replace_with_water(child)
        child.z, child.y, child.x = self.get_coords(parent)
        self.sync_coords(child)

    def get_coords(self, thing):
        return thing.z, thing.y, thing.x

    def place_coords(self, thing, z, y, x):
        self.world[z][y][x] = thing

    def step(self, direc, thing):
        moveable = self.can_move(thing)
        if moveable and direc in moveable and thing.can_move:
            self.replace_with_water(thing)
            if direc == 1:
                thing.y -= 1
            elif direc == 2:
                thing.x -= 1
            elif direc == 3:
                thing.y += 1
            elif direc == 4:
                thing.x += 1
            elif direc == 5:
                thing.z += 1
            elif direc == 6:
                thing.z -= 1
            self.sync_coords(thing)
            if isinstance(thing, entity.ROV):
                thing.power_tick(20)
        else:
            print("Thunk.")

    def grab(self, item, thing):
        if item.can_grab and thing.check_inventory(item):
            self.match_coords(item, thing)
            thing.inventory.append(item)
            thing.refresh_inventory()
            print("Picked up " + item.s_name())
            thing.power_tick(10)
        else:
            print("It's stuck!")

    def drop(self):
        player.show_inventory()
        item = str(input("Choose an item to drop: "))
        for i in player.inventory:
            if i.s_name() == item:
                self.match_coords(i, player)
                avail = self.can_move(player)
                direc = random.randint(1, 5)
                if direc == 1:
                    i.y -= 1
                elif direc == 2:
                    i.x -= 1
                elif direc == 3:
                    i.y += 1
                elif direc == 4:
                    i.x += 1
                self.sync_coords(i)
                player.inventory.remove(i)
                player.refresh_inventory()
                player.power_tick(10)
                break
        else:
            print("You don't have a " + item + "!")

    def show_commands(self):
        print(self.commands_dict)

    def print_hud(self, thing):
        perc = thing.cell.get_percentage()
        count = int(perc / 10)
        print("Power: <" + ("=" * count) + (" " * (10 - count)) + ">")
        print("Z: " + str(thing.z) + " Y: " + str(thing.y) + " X: " + str(thing.x))
        print("Inventory: V" + str(thing.inventory_vol) + "/W" + str(thing.inventory_weight))

    def handle_input(self, inp):
        clear()
        if inp.startswith("Q"):
            self.step(5, player)
        elif inp.startswith("W"):
            self.step(1, player)
        elif inp.startswith("E"):
            self.step(6, player)
        elif inp.startswith("A"):
            self.step(2, player)
        elif inp.startswith("S"):
            self.step(3, player)
        elif inp.startswith("D"):
            self.step(4, player)
        elif inp.startswith("U"):
            player.use()
        elif inp.startswith("?"):
            self.show_commands()
        elif inp.startswith("I"):
            player.show_inventory()
        elif inp.startswith("G"):
            available = player.key_list(self.get_adjacent(player))
            print("Adjacent items: ")
            for key, value in available.items():
                print(key + ": " + value.s_name())
            chose = str(input("Choose which item to grab > "))
            valid = False
            for key, value in available.items():
                if chose == key:
                    self.grab(value, player)
                    valid = True
                    break
            if not valid:
                print("Invalid item!")
        elif inp.startswith("F"):
            self.drop()
        else:
            print("Invalid command. Enter '?' for a list of commands.")
        #self.tick()

def options_get_value():
    return int(input("Enter a value for " + str(editing) + " > "))

def clear():
    os.system('cls')

def main():
    global WORLD_Z
    global WORLD_Y
    global WORLD_X
    global PLAYER_VIEW_Y
    global PLAYER_VIEW_X
    global DEBUG
    global player
    while True:
        print("1. Start")
        print("2. Options")
        choice = str(input("Enter your choice (Start/Options) > ")).title()
        if choice == "Start":
            globe = World(WORLD_Z, WORLD_Y, WORLD_X, PLAYER_VIEW_Y,
                            PLAYER_VIEW_X, DEBUG)

            player = globe.player
            while True:
                globe.print_world(player)
                globe.print_hud(player)
                globe.handle_input(str(input(">> ")).upper())

        elif choice == "Options":
            print("Z-levels: " + str(WORLD_Z))
            print("Y-levels: " + str(WORLD_Y))
            print("X-levels: " + str(WORLD_X))
            print("Player Y view size: " + str(PLAYER_VIEW_Y))
            print("Player X view size: " + str(PLAYER_VIEW_X))
            editing = str(input("Choose which setting to change, or enter 'Exit' to go back to the menu > ")).title()
            try:
                if editing == "Z-Levels":
                    WORLD_Z = options_get_value()
                elif editing == "Y-Levels":
                    WORLD_Y = options_get_value()
                elif editing == "X-Levels":
                    WORLD_X = options_get_value()
                elif editing == "Player Y View Size":
                    PLAYER_VIEW_Y = options_get_value()
                elif editing == "Player X View Size":
                    PLAYER_VIEW_X = options_get_value()
            except:
                pass

while True:
    try:
        main()
    except:
        print("Fatal Error. Returning to menu...")
        logging.exception("Exception")
