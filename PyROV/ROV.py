# 1 = north
# 2 = east
# 3 = south
# 4 = west
# 5 = up
# 6 = down

class ROV:
    inventory = []
    obstList = ["#", "%"]
    grabList = ["*", "?", "!", "$"]

    def __init__(self, z, x, y, comp):
        self.z = z
        self.x = x
        self.y = y
        self.components = comp

    def move(self, dir, world):
        moveable = self.can_move(world)
        try:
            if moveable is not None and dir in moveable:
                if dir == 1:
                    self.y += 1
                elif dir == 2:
                    self.x += 1
                elif dir == 3:
                    self.y -= 1
                elif dir == 4:
                    self.x -= 1
                elif dir == 5:
                    self.z += 1
                elif dir == 6:
                    self.z -= 1
            world[self.z][self.x][self.y] = "@"
        except:
            return None

    def get_coords(self):
        return [self.z self.x, self.y]


    def can_move(world):
        moveable = []
        if world[self.z][self.x][self.y + 1] not in self.obst:
            moveable.append(1)
        if world[self.z][self.x + 1][self.y] not in self.obst:
            moveable.append(2)
        if world[self.z][self.x][self.y - 1] not in self.obst:
            moveable.append(3)
        if world[self.z][self.x - 1][self.y] not in self.obst:
            moveable.append(4)
        if world[self.z + 1][self.x][self.y] not in self.obst:
            moveable.append(5)
        if world[self.z - 1][self.x][self.y] not in self.obst:
            moveable.append(6)
        if len(moveable) == 0:
            return None
        else:
            return moveable
        
