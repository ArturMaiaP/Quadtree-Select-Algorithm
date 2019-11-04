

# The Node class represents a quadrant and the points inside it.
class Node():
    def __init__(self, xMin, yMin, xMax, yMax, points,number):
        self.xMin = xMin
        self.yMin = yMin
        self.xMax = xMax
        self.yMax = yMax
        self.points = points
        self.nodeNumber = number
        self.childrens = []

    def getPoints(self):
        return self.points

    def getxLen(self):
        return abs(self.xMax) + abs(self.xMin)

    def getyLen(self):
        return abs(self.yMax) + abs(self.yMin)

    def getxMin(self):
        return self.xMin

    def getyMin(self):
        return self.yMin

    def getxMax(self):
        return self.xMax

    def getyMax(self):
        return self.yMax

    def getNumberPoints(self):
        return len(self.points)

    def getChildrens(self):
        return self.childrens

    def removePt(self,pt):
        self.points.remove(pt)