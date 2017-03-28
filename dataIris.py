import math

class Data(object):

    def __init__(self,index,a, b,c,d, classification):
        self.index = index
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.classification = classification

    def distance(self, neighbor):
        return math.sqrt( math.pow(float(self.a)-float(neighbor.a), 2) + math.pow(float(self.b)- float(neighbor.b), 2) + math.pow(float(self.c) - float(neighbor.c) , 2) + math.pow(float(self.d) - float(neighbor.d), 2)  )
