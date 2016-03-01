class Object:
    name = "Example"
    icon = "*"
    can_grab = True
    passable = True

    def __init__(self, x, y, z):
        self.z = z
        self.x = x
        self.y = y
