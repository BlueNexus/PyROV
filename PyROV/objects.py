class Object:
    
    def __init__(self, oName, oDesc, oSym, oVol, x, y, z):
        self.name = oName
        self.desc = oDesc
        self.symbol = oSym
        self.volume = oVol
        self.z = z
        self.x = x
        self.y = y
        self.inside = None
