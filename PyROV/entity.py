import blocks
import objects
import random

class Entity:
    can_grab = False
    name = ""
    inventory = []
    icon = "e"
    can_move = True

    def __init__(self, z, y, x, world):
        self.z = z
        self.y = y
        self.x = x

    def get_coords(self):
        return self.z, self.y, self.x

class ROV(Entity):
    name = "ROV"
    icon = "@"

    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x
        self.cell = objects.CellBasic(self.z, self.y, self.x)

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

