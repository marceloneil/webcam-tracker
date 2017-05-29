class Hotspot:
    """Hotspot thingy"""

    def __init__(self, p1, p2):
        self.minx, self.maxx = sorted([p1[0], p2[0]])
        self.miny, self.maxy = sorted([p1[1], p2[1]])

    def check(self, point):
        x, y = point
        if (self.minx <= x <= self.maxx) and (self.miny <= y <= self.maxy):
            return True
        return False
