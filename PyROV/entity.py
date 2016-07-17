import blocks
import objects
import random
import time
import string

charset = list(string.printable)
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

    def __init__(self, z, y, x, world):
        self.z = z
        self.y = y
        self.x = x

    def get_coords(self):
        return self.z, self.y, self.x

    def act(self):
        pass

    def __repr__(self):
        return(self.icon)


class ROV(Entity):
    name = "ROV"
    icon = "@"
    inventory = []
    inventory_vol = 0
    inventory_weight = 0

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

    def refresh_inventory(self):
        self.inventory_vol = 0
        self.inventory_weight = 0
        for item in self.inventory:
            self.inventory_vol += item.vol
            self.inventory_weight += item.weight

    def check_inventory(self, item):
        if (self.inventory_vol +
            item.vol) <= 100 and (self.inventory_weight +
                                  item.weight) <= 50:
            return True
        else:
            print("You've got too much in your inventory!")
            return False

    def power_tick(self, cost):
        self.cell.power -= cost
        if self.cell.power <= 0:
            self.shutdown()

    def show_inventory(self):
        print("Items in inventory: ")
        dict_inventory = self.key_list(self.inventory)
        for key, value in dict_inventory.items():
            print(key + ": " + value.s_name())

    def get_keyed_inventory(self):
        print("Items in inventory: ")
        dict_inventory = self.key_list(self.inventory)
        for key, value in dict_inventory.items():
            print(key + ": " + value.s_name())
        return(dict_inventory)

    def key_list(self, old_list):
        dictified = {}
        for index, item in enumerate(old_list):
            dictified[charset[index]] = item
        return dictified

    def use(self):
        inv = self.get_keyed_inventory()
        choice = str(input("Choose an item to use: "))
        for key, value in inv.items():
            if key == choice:
                value.activate(self)
