class Object:
    name = "Example"
    icon = "*"
    can_grab = True
    passable = True
    useable = False
    vol = 1
    weight = 1

    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x

    def act(self):
        pass

class Cell(Object):
    name = "Cell"
    icon = "="
    total_power = 1000
    
    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x
        self.float_power = float(self.total_power)
        self.power = self.float_power

    def activate(self, user):
        user.inventory.append(user.cell)
        user.cell = self
        user.inventory.remove(self)
        user.refresh_inventory()

    def get_percentage(self):
        return(int(((self.power / self.float_power) * 100)))

class CellBasic(Cell):
    name = "PC-Lite Cell"
    vol = 1
    weight = 2

class CellMedium(Cell):
    name = "PC-2K Cell"
    total_power = 2000
    vol = 4
    weight = 8

class CellLarge(Cell):
    name = "PC-4K Cell"
    total_power = 4000
    vol = 8
    weight = 16

class CellXL(Cell):
    name = "PB-16K Battery"
    total_power = 16000
    vol = 30
    weight = 50
