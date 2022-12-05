from Vectors import *


class Tower(Point3):
    def __init__(self, xyz, dist=None):
        super().__init__(xyz)
        self.dist = dist

    def getDist(self):
        return self.dist

    def setDist(self, dist):
        self.dist = dist

    def get(self):
        return self.x, self.y, self.z, self.dist


class Towers:
    def __init__(self, towers):
        self.towers = towers
