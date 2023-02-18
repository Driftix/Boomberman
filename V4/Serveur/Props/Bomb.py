class Bomb:
    def __init__(self,r,q,l):
        self.className = "bomb"
        self.radius = r
        self.quantity = q
        self.loadTime = l
    def getRadius(self):
        return self.radius
    def addRadius(self,r):
        self.radius += r
    def setRadius(self,r):
        self.radius = r


