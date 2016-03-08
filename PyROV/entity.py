import blocks
import objects
import random
import time

# 1 = north
# 2 = east
# 3 = south
# 4 = west
# 5 = up
# 6 = down


class Entity:
    can_grab = False
    name = ""
    icon = "e"
    can_move = True

    def __init__(self, z, x, y, world):
        self.z = z
        self.x = x
        self.y = y

    def get_coords(self):
        return self.z, self.x, self.y


    def get_adjacent_items(self, world):
        adjacent = []
        adjacent.append(world[self.z][self.x][self.y + 1])
        adjacent.append(world[self.z][self.x][self.y - 1])
        adjacent.append(world[self.z][self.x][self.x + 1])
        adjacent.append(world[self.z][self.x][self.x - 1])
        adjacent.append(world[self.z][self.x + 1][self.y + 1])
        adjacent.append(world[self.z][self.x - 1][self.y + 1])
        adjacent.append(world[self.z][self.x + 1][self.y - 1])
        adjacent.append(world[self.z][self.x - 1][self.y - 1])
        for thing in adjacent:
            if isinstance(thing, blocks.Block):
                adjacent.remove(thing)
            if thing == self:
                adjacent.remove(thing)
        return adjacent


class ROV(Entity):
    name = "ROV"
    inventory = []
    icon = "@"

    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y
        self.cell = objects.CellBasic(self.z, self.x, self.y)

    def move(self, direc, world):
        moveable = self.can_move(world)
        if self.can_move:
            if moveable and direc in moveable:
                world[self.z][self.x][self.y] = blocks.Water(self.z, self.x, self.y)
                if direc == 1:
                    self.y += 1
                elif direc == 2:
                    self.x += 1
                elif direc == 3:
                    self.y -= 1
                elif direc == 4:
                    self.x -= 1
                elif direc == 5:
                    self.z += 1
                elif direc == 6:
                    self.z -= 1
                world[self.z][self.x][self.y] = self
            else:
                print("Thunk.")
            self.power_tick(10)
        else:
            print("You can't move!")

    def shutdown(self):
        self.can_move = False
        print("Game Over.")
        time.sleep(3)
        exit()

    def power_tick(self, cost):
        self.cell.power -= cost
        if self.cell.power <= 0:
            self.shutdown()

    def show_inventory(self):
        print("Items in inventory: ")
        for i in self.inventory:
            print(i.name)

    def use(self):
        self.show_inventory()
        choice = str(raw_input("Choose an item to use: "))
        for i in self.inventory:
            if i.name == choice:
                i.activate()

    def grab(self, item, world):
        if item.can_grab:
            world[item.z][item.x][item.y] = blocks.Water(item.z, item.x, item.y)
            item.z, item.x, item.y = self.get_coords()
            self.inventory.append(item)
            print("Picked up " + item.name)
            self.power_tick(5)
        else:
            print("It's stuck!")
    
    def drop(self, world):
        self.show_inventory()
        item = str(raw_input("Choose an item to drop: "))
        for i in self.inventory:
            if i.name == item:
                i.z, i.x, i.y = self.get_coords()
                avail = self.can_move(world)
                direc = random.randint(1, 5)
                if direc == 1:
                    i.y += 1
                elif direc == 2:
                    i.x += 1
                elif direc == 3:
                    i.y -= 1
                elif direc == 4:
                    i.x -= 1
                world[item.z][item.x][item.y] = item
                self.inventory.remove(item)
                self.power_tick(5)
                break
        else:
            print("You don't have a " + item + "!")
