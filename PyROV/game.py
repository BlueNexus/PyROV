import entity
import blocks
import objects
import random

player = None

''' Everything is broken. Will fix soon
Todo: 
Move grabbing and dropping into world
Fix x and y being the wrong way round
Unbreak all the stuff
'''


class World:
	
    commands_dict = {"Q": "Move up", "W": "Move forward", "E": "Move down",
            "A": "Move left", "S": "Move back", "D": "Move right",
            "U": "Use item", "?": "Show commands", "I": "Show inventory",
            "G": "Grab", "F": "Drop"}
	commands_list = ["Q", "W", "E", "A", "S", "D", "U", "?", "I", "G", "F"]
	WORLD_Z = 20
	WORLD_X = 40
	WORLD_Y = 40
	WORLDGEN_ROCK_CHANCE = 15
	WORLDGEN_OBJECT_CHANCE = 1
	PLAYER_VIEW_X = 6
	PLAYER_VIEW_Y = 6
	world = []

    def __init__(self):
        self.make_world(self.WORLD_Z, self.WORLD_X, self.WORLD_Y)

    def make_world(self, z, x, y):
        working = []
        for plane in range(z):
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
        global player
        self.world = working
        print("Creating the player...")
        start_z = z / 2
        start_x = x / 2
        start_y = y / 2
        player = entity.ROV(start_z, start_x, start_y)
        self.world[player.z][player.x][player.y] = player
        print("Generation complete!")

	def get_view_extents(self, thing, x, y):
		pass

    def print_world(self, thing):
    	cur_Z = thing.z
    	cur_X = thing.x
    	cur_Y = thing.y
        working = self.world[cur_Z]
        north, east, south, west = self.get_view_extents(thing, cur_X, cur_Y)
        for row in range(cur_X - north, cur_X + south):
            work_X = working[row]
            final_X = []
            for col in range(cur_Y - west, cur_Y + east):
                final_X.append(work_X[col].icon)
            final_X_joined = ' '.join(final_X)
            print(fX_joined)

	def can_move(self, thing):
        moveable = []
        if self.world[thing.z][thing.x][thing.y + 1].passable:
            moveable.append(1)
        if self.world[thing.z][thing.x + 1][thing.y].passable:
            moveable.append(2)
        if self.world[thing.z][thing.x][thing.y - 1].passable:
            moveable.append(3)
        if self.world[thing.z][thing.x - 1][thing.y].passable:
            moveable.append(4)
        if self.world[thing.z + 1][thing.x][thing.y].passable:
            moveable.append(5)
        if self.world[thing.z - 1][thing.x][thing.y].passable:
            moveable.append(6)
        return moveable

	def replace_with_water(self, thing):
		self.world[thing.z][thing.x][thing.y] = blocks.Water(thing.z, thing.x, thing.y)

	def sync_thing(self, thing):
		self.world[thing.z][thing.x][thing.y] = thing

	def place_thing(self, thing, z, x, y):
		self.world[z][x][y] = thing

    def step(self, direc, thing):
        moveable = self.can_move(matter)
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
            self.sync_zxy(thing)
        else:
            print("Thunk.")

	def show_commands(self):
    	print(self.commands_dict)


	def handle_input(self, inp):
    	if inp in self.commands_list:
        	if inp == "Q":
            	self.step(5, player)
        	elif inp == "W":
            	self.step(4, player)
        	elif inp == "E":
            	self.step(6, player)
        	elif inp == "A":
            	self.step(3, player)
        	elif inp == "S":
            	self.step(2, player)
        	elif inp == "D":
            	self.step(1, player)
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

while True:
    print("1. Start")
    print("2. Options")
    choice = str(raw_input("Enter your choice (Start/Options) > ")).title()
    if choice == "Start":
    	globe = World()
        while True:
            globe.print_world(player)
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
