class Block:
    name = ""
    icon = "#"
    passable = False
    can_grab = False
    
    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x

    def act(self):
        pass

class Water(Block):
    name = "Water"
    icon = "."
    passable = True

class Rock(Block):
    name = "Rock Wall"
