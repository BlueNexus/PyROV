class Block:
    name = ""
    icon = "#"
    passable = False
    
    def __init__(self, z, x, y):
        self.z = z
        self.x = x
        self.y = y

class Water(Block):
    name = "Water"
    icon = "."
    passable = True
