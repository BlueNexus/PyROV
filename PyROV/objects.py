class Object:
    name = "Example"
    icon = "*"
    can_grab = True
    passable = True

    def __init__(self, x, y, z):
        self.z = z
        self.x = x
        self.y = y

class Cell(Object):
    name = "Cell"
    icon = "="
    total_power = 1000
    
    def __init__(self, x, y, z):
        self.z = z
        self.x = x
        self.y = y
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
    name = "PC-16K Battery"
    total_power = 16000
    
