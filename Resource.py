import sys
import node

class Tree:
  def __init__(self, myMap, xPos, yPos, length):
    self.length = length
    self.myMap = myMap
    self.x = xPos
    self.y = yPos
    self.myMap.putExistance(self, xPos, yPos)
