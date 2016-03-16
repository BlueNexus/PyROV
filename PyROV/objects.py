class Object:
    name = "Example"
    icon = "*"
    can_grab = True
    passable = True
    useable = False

    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x

class Cell(Object):
    name = "Cell"
    icon = "="
    total_power = 1000
    useable = True
    
    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x
        self.power = self.total_power

class CellBasic(Cell):
    name = "PC-Lite Cell"

class CellMedium(Cell):
    name = "PC-2K Cell"
    total_power = 2000

class CellLarge(Cell):
    name = "PC-4K Cell"
    total_power = 4000

class CellXL(Cell):
    name = "PB-16K Battery"
    total_power = 16000
    
