import sys
import node

class Person:
    def __init__(self, name, myMap, xPos, yPos):
        self.name = name
        self.x = xPos
        self.y = yPos
        self.myMap = myMap
        self.myMap.putExistance(self, xPos, yPos)
        self.generateBody();

    def __str__(self):
        return "%s exists in pos (%d, %d)" %(self.name, self.x, self.y)

    def move(self, direction):
        newX, newY = self.myMap.movePerson(self, direction)
        if self.x == newX:
            print('can not move there')
        else:
          self.x = newX
          self.y = newY

    def generateBody(self):
      self.body = {}
      self.body['Head'] = BodyPart()
      self.body['Neck'] = BodyPart()
      self.body['Left Shoulder'] = BodyPart()
      self.body['Right Shoulder'] = BodyPart() 
      self.body['Left Wrist'] = BodyPart()
      self.body['Right Wrist'] = BodyPart()
      self.body['Left Hand'] = BodyPart()
      self.body['Right Hand'] = BodyPart()
      self.body['Body'] = BodyPart()
      self.body['Back'] = BodyPart()
      self.body['Waist'] = BodyPart()      
      self.body['Lower Body'] = BodyPart()
      self.body['Left Knee'] = BodyPart()
      self.body['Right Knee'] = BodyPart()
      self.body['Left Feet'] = BodyPart()
      self.body['Right Feet'] = BodyPart()
      
class BodyPart:
    def __init__(self):
      self.gear = None
      self.health = 100
