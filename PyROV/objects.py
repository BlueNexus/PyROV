class Block:
    name = ""
    icon = "#"
    passable = False
    can_grab = False
    debug = False
    
    def __init__(self, z, y, x):
        self.z = z
        self.y = y
        self.x = x

    def act(self):
        pass

    def __repr__(self):
        return(self.icon)

class Water(Block):
    name = "Water"
    icon = "."
    passable = True

class Rock(Block):
    name = "Rock Wall"
