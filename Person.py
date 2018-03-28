import sys
import node
import pygame
import math
import time
import Resources

class Person(pygame.sprite.Sprite):
    def __init__(self, name, myMap, location, playerView, layer, group):
        self._layer = layer
        self.angle = 270
        self.name = name
        self.myMap = myMap
        self.generateBody()
        self.attributes = {}
        self.playerView = playerView
        self.attributes["Strength"] = 40
        self.image = pygame.image.load('img/Bot.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        print(self.rect)
        #position relative to the map
        self.pos = pygame.math.Vector2(location)
        #position relative to the window
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        #tile position
        self.position = self.myMap.cordsConversion((self.pos.x+3)/42, (self.pos.y+3)/42)
        self.vel = pygame.math.Vector2(0, 0)
        self.moveProgress = pygame.math.Vector2(0, 0)
        self.path = []
        self.currentPath = None
        self.newOrders = pygame.math.Vector2(0, 0)
        self.harvesting = None
        self.focusTarget = None
        self.destroy = False
        self.actionProgress = 0
        pygame.sprite.Sprite.__init__(self, group)

    def updatePosition(self):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')

    def definePath(self):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        destination = self.myMap.cordsConversion(math.floor(self.newOrders.x/42), math.floor(self.newOrders.y/42))
        self.path = self.myMap.shortestPath(self.position, destination, self)
        self.newOrders = pygame.math.Vector2(0, 0)

    def harvestProgress(self):
        if self.harvesting:
            self.harvesting.durability -= 1
            if self.harvesting.durability < 1:
                if self.position+1 == self.harvesting.position:
                    self.harvesting.destroy = "east"
                elif self.position-1 == self.harvesting.position:
                    self.harvesting.destroy = "west"
                elif self.position-100 == self.harvesting.position:
                    self.harvesting.destroy = "north"
                elif self.position+100 == self.harvesting.position:
                    self.harvesting.destroy = "south"
                self.harvesting = None

    def movingAction(self):
        if self.Body['Left Hand'].item and self.Body['Left Hand'].item.carryWeight < self.Body['Left Hand'].item.weight or self.Body['Right Hand'].item and self.Body['Right Hand'].item.carryWeight < self.Body['Right Hand'].item.weight:
            print('Too Heavy')
            self.currentPath = None
            self.path = []
        else:
            if isinstance(self.currentPath, int):
                rotation = 0
                self.myMap.addEdgesFrom(self.position, 'all')
                self.myMap.removeEdgesFrom(self.currentPath, 'into')
                if math.floor(self.position + 1) == self.currentPath:
                    if self.angle == 0:
                        self.moveProgress.x = 42
                    elif self.angle == 90:
                        self.rotate(-90)
                    elif self.angle == 270:
                        self.rotate(90)
                    elif self.angle == 180:
                        self.rotate(90)
                elif math.floor(self.position - 1) == self.currentPath:
                    if self.angle == 0:
                        self.rotate(90)
                    elif self.angle == 90:
                        self.rotate(90)
                    elif self.angle == 270:
                        self.rotate(-90)
                    elif self.angle == 180:
                        self.moveProgress.x = -42
                elif math.floor(self.position - 100) == self.currentPath:
                    if self.angle == 0:
                        self.rotate(90)
                    elif self.angle == 90:
                        self.moveProgress.y = -42
                    elif self.angle == 270:
                        self.rotate(90)
                    elif self.angle == 180:
                        self.rotate(-90)
                elif math.floor(self.position + 100) == self.currentPath:
                    if self.angle == 0:
                        self.rotate(-90)
                    elif self.angle == 90:
                        self.rotate(90)
                    elif self.angle == 270:
                        self.moveProgress.y = 42
                    elif self.angle == 180:
                        self.rotate(90)
            elif isinstance(self.currentPath, str):
                if math.floor(self.position + 1) == int(self.currentPath[1:]):
                    if self.angle == 0:
                        self.currentPath = self.position
                    elif self.angle == 90:
                        self.rotate(-90)
                    elif self.angle == 270:
                        self.rotate(90)
                    elif self.angle == 180:
                        self.rotate(90)
                elif math.floor(self.position - 1) == int(self.currentPath[1:]):
                    if self.angle == 0:
                        self.rotate(90)
                    elif self.angle == 90:
                        self.rotate(90)
                    elif self.angle == 270:
                        self.rotate(-90)
                    elif self.angle == 180:
                        self.currentPath = self.position
                elif math.floor(self.position - 100) == int(self.currentPath[1:]):
                    if self.angle == 0:
                        self.rotate(90)
                    elif self.angle == 90:
                        self.currentPath = self.position
                    elif self.angle == 270:
                        self.rotate(90)
                    elif self.angle == 180:
                        self.rotate(-90)
                elif math.floor(self.position + 100) == int(self.currentPath[1:]):
                    if self.angle == 0:
                        self.rotate(-90)
                    elif self.angle == 90:
                        self.rotate(90)
                    elif self.angle == 270:
                        self.currentPath = self.position
                    elif self.angle == 180:
                        self.rotate(90)


    def update(self):
        self.rect.x = self.pos.x + self.playerView.cameraPos.x
        self.rect.y = self.pos.y + self.playerView.cameraPos.y
        if self.moveProgress.x == 0 and self.moveProgress.y == 0:
            self.updatePosition()
        if not self.currentPath:
            if self.newOrders.x != 0 and self.newOrders.y != 0 and self.position != self.myMap.cordsConversion(math.floor(self.newOrders.x/42), math.floor(self.newOrders.y/42)):
                self.definePath()
            elif self.newOrders.x == 0 and self.newOrders.y == 0 and not self.path:
                self.harvestProgress()
                #not harvesting log
            if self.path:
                self.currentPath = self.path.pop()
        else:
            if self.position == self.currentPath:
                self.currentPath = None
            else:
                if self.moveProgress.x == 0 and self.moveProgress.y == 0:
                    self.movingAction()
                else:
                    self.move()

    def action(self):
        if isinstance(self.focusTarget, Resources.Item):
            self.pickup(self.focusTarget)
            if self.focusTarget.name == "Log":
                if self.Body['Right Hand'].item.name == "Saw" or self.Body['Left Hand'].item.name == "Saw":
                    self.harvesting = self.focusTarget
        elif isinstance(self.focusTarget, Resources.Tree):
            self.harvesting = self.focusTarget

    def stopAction(self):
        self.harvesting = None
        self.newOrders = pygame.math.Vector2(0, 0)
        self.path = []

    def pickup(self, item):
      if item.weight < self.attributes['Strength']:
          if not self.Body['Right Hand'].item:
            self.Body['Right Hand'].item = item
            item.carryWeight = self.attributes['Strength']
            self.myMap.entityList.remove(item)
            self.itemReorientation(item)       
          elif not self.Body['Left Hand'].item:
            self.Body['Left Hand'].item = item
            item.carryWeight = self.attributes['Strength']
            self.myMap.entityList.remove(item)
            self.itemReorientation(item)
      elif item.weight < self.attributes['Strength']*2:
          if not self.Body['Right Hand'].item and not self.Body['Left Hand'].item:
            self.Body['Right Hand'].item = item
            self.Body['Left Hand'].item = item
            item.carryWeight = self.attributes['Strength']*2
            self.myMap.entityList.remove(item)
            self.itemReorientation(item)

    def itemReorientation(self, item):
        if item.angle%360 == 90:
            item.rotate(-90)
        elif item.angle%360 == 180:
            item.rotate(90)
            item.rotate(90)
        elif item.angle%360 == 270:
            item.rotate(90)
        

    def dropItem(self, getHand):
        hand = None
        placable = True
        if self.angle == 270:
            if self.myMap.placementChecker(self.position+100, int(self.Body[getHand].item.rect.width/42), int(self.Body[getHand].item.rect.height/42), 270):
                self.Body[getHand].item.pos = self.pos + (3, 45)
            else:
                placable = False
        elif self.angle == 90:
            if self.myMap.placementChecker(self.position-100, int(self.Body[getHand].item.rect.width/42), int(self.Body[getHand].item.rect.height/42), 90):
                self.Body[getHand].item.pos = self.pos - ((int(self.Body[getHand].item.rect.height)), (int(self.Body[getHand].item.rect.width))) + (45, 3)
            else:
                placable = False
        elif self.angle == 0:
            if self.myMap.placementChecker(self.position+1, int(self.Body[getHand].item.rect.width/42), int(self.Body[getHand].item.rect.height/42), 0):
                self.Body[getHand].item.pos = self.pos + (45, 3)
            else:
                placable = False
        elif self.angle == 180:
            if self.myMap.placementChecker(self.position-1, int(self.Body[getHand].item.rect.width/42), int(self.Body[getHand].item.rect.height/42), 180):
                self.Body[getHand].item.pos = self.pos - ((int(self.Body[getHand].item.rect.width),(int(self.Body[getHand].item.rect.height)))) + (3, 45)
            else:
                placable = False
        if placable:
            while (self.Body[getHand].item.angle != self.angle):
                self.Body[getHand].item.rotate(90)
            self.Body[getHand].item.position = self.myMap.cordsConversion(self.Body[getHand].item.pos.x/42, self.Body[getHand].item.pos.y/42)
            self.Body[getHand].item.rect.x = self.Body[getHand].item.pos.x
            self.Body[getHand].item.rect.y = self.Body[getHand].item.pos.y
            self.myMap.addEntity(self.Body[getHand].item)
            self.Body[getHand].item.carryWeight = 0
            if getHand == "Left Hand" or getHand == "Both":                
                self.Body['Left Hand'].item = None
            if getHand == "Right Hand" or getHand == "Both":
                self.Body['Right Hand'].item = None
        else:
            print('Unable to place item')

    def selected(self):
        print("%s is selected" %(self.name))
            
    def move(self):
        if self.moveProgress.x > 0:
            self.pos += self.moveHelper("x", 1)
        elif self.moveProgress.x < 0:
            self.pos += self.moveHelper("x", -1)
        elif self.moveProgress.y > 0:
            self.pos += self.moveHelper("y", 1)
        elif self.moveProgress.y < 0:
            self.pos += self.moveHelper("y", -1)
        #self.rect.topleft = self.pos

    def moveHelper(self, axis, offset):
        if axis == "x":
            # - 3*offset
            if self.moveProgress.x != 0:
                velocity = pygame.math.Vector2(3*offset, 0)
                self.moveProgress.x -= 3*offset
        elif axis == "y":
            if self.moveProgress.y != 0:
                velocity = pygame.math.Vector2(0, 3*offset)
                self.moveProgress.y -= 3*offset
        return velocity
            
    def getDestination(self, goal):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        destination = self.myMap.cordsConversion(math.floor(goal.x/42), math.floor(goal.y/42))
        self.path = self.myMap.shortestPath(self.position, destination)

    def rotate(self, amount):
        self.angle = (self.angle + int(amount))%360
        self.image = self.rotateHelper(self.image, amount)

    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def generateBody(self):
      self.Body = {}
      self.Body['Head'] = BodyPart()
      self.Body['Head'].pos = pygame.math.Vector2(63, 5)
      self.Body['Neck'] = BodyPart()
      self.Body['Neck'].pos = pygame.math.Vector2(63, 37)
      self.Body['Left Shoulder'] = BodyPart()
      self.Body['Left Shoulder'].pos = pygame.math.Vector2(30, 37)
      self.Body['Right Shoulder'] = BodyPart()
      self.Body['Right Shoulder'].pos = pygame.math.Vector2(96, 37)
      self.Body['Left Wrist'] = BodyPart()
      self.Body['Left Wrist'].pos = pygame.math.Vector2(30, 69)
      self.Body['Right Wrist'] = BodyPart()
      self.Body['Right Wrist'].pos = pygame.math.Vector2(96, 69)
      self.Body['Left Hand'] = BodyPart()
      self.Body['Left Hand'].pos = pygame.math.Vector2(30, 101)
      self.Body['Right Hand'] = BodyPart()
      self.Body['Right Hand'].pos = pygame.math.Vector2(96, 101)
      self.Body['Body'] = BodyPart()
      self.Body['Body'].pos = pygame.math.Vector2(63, 101)
      self.Body['Back'] = BodyPart()
      self.Body['Back'].pos = pygame.math.Vector2(63, 69)
      self.Body['Left Waist'] = BodyPart()
      self.Body['Left Waist'].pos = pygame.math.Vector2(30, 133)
      self.Body['Right Waist'] = BodyPart()
      self.Body['Right Waist'].pos = pygame.math.Vector2(96, 133)
      self.Body['Lower Body'] = BodyPart()
      self.Body['Lower Body'].pos = pygame.math.Vector2(63, 133)
      self.Body['Left Knee'] = BodyPart()
      self.Body['Left Knee'].pos = pygame.math.Vector2(30, 165)
      self.Body['Right Knee'] = BodyPart()
      self.Body['Right Knee'].pos = pygame.math.Vector2(96, 165)
      self.Body['Left Feet'] = BodyPart()
      self.Body['Left Feet'].pos = pygame.math.Vector2(30, 197)
      self.Body['Right Feet'] = BodyPart()
      self.Body['Right Feet'].pos = pygame.math.Vector2(96, 197)

class BodyPart:
    def __init__(self):
      self.gear = None
      self.health = 100
      self.item = None
      self.pos = pygame.math.Vector2(0, 0)
