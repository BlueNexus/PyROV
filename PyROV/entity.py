import blocks
import objects
import random

# 1 = north
# 2 = east
# 3 = south
# 4 = west
# 5 = up
# 6 = down


class Entity:
    icon = "e"
    
    def __init__(self, z, x, y, world):
        self.z = z
        self.x = x
        self.y = y

    def move(self, direc, world):
        moveable = self.can_move(world)
        if moveable and direc in moveable:
            world[self.z][self.x][self.y] = blocks.Water()
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

    def get_coords(self):
        return self.z, self.x, self.y

    def can_move(self, world):
        moveable = []
        if world[self.z][self.x][self.y + 1].passable == True:
            moveable.append(1)
        if world[self.z][self.x + 1][self.y].passable == True:
            moveable.append(2)
        if world[self.z][self.x][self.y - 1].passable == True:
            moveable.append(3)
        if world[self.z][self.x - 1][self.y].passable == True:
            moveable.append(4)
        if world[self.z + 1][self.x][self.y].passable == True:
            moveable.append(5)
        if world[self.z - 1][self.x][self.y].passable == True:
            moveable.append(6)
        return moveable

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
        return adjacent

class ROV(Entity):
    inventory = []
    icon = "@"

    def show_inventory(self):
        print("Items in inventory: ")
        for i in self.inventory:
            print(i.name)

    def grab(self, item, world):
        if item.can_grab:
            world[item.z][item.x][item.y] = block.Water()
            item.z, item.x, item.y = None
            self.inventory.append(item)
            print("Picked up " + item.name)
    
    def drop(self, world):
        self.show_inventory()
        item = str(raw_input("Choose an item to drop: "))
        if item in self.inventory:
            item.z, item.x, item.y = self.get_coords()
            avail = self.can_move(world)
            direc = random.randint(1, 5)
            if direc == 1:
                item.y += 1
            elif direc == 2:
                item.x += 1
            elif direc == 3:
                item.y -= 1
            elif direc == 4:
                item.x -= 1
            world[item.z][item.x][item.y] = item
            self.inventory.remove(item)
