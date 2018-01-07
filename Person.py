import sys
import node
import pygame
import math
import time

class Person(pygame.sprite.Sprite):
    def __init__(self, name, myMap, location, playerView):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 270
        self.name = name
        self.myMap = myMap
        self.generateBody();
        self.image = pygame.image.load('img/Bot.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
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
        
    def draw_self(self, window, playerView):
        window.blit(self.image, self.pos+playerView.cameraPos)
            
    def update(self, playerView):
        if not self.currentPath:
            if self.newOrders.x != 0 and self.newOrders.y != 0:
                self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))                
                destination = self.myMap.cordsConversion(math.floor(self.newOrders.x/42), math.floor(self.newOrders.y/42))                     
                self.path = self.myMap.shortestPath(self.position, destination)
                self.newOrders = pygame.math.Vector2(0, 0)
            if self.path:
                self.currentPath = self.path.pop()               
        else:
            if self.position == self.currentPath:
                self.currentPath = None
            else:
                if self.moveProgress.x == 0 and self.moveProgress.y == 0:
                    self.myMap.addEdgesFrom(self.position, 'into') 
                    self.myMap.removeEdgesFrom(self.currentPath, 'into')
                    #not creating the edges to go into
                    self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))                    
                    if math.floor(self.position + 1) == self.currentPath:
                        self.moveProgress.x = 45
                    elif math.floor(self.position - 1) == self.currentPath:
                        self.moveProgress.x = -45
                    elif math.floor(self.position - 100) == self.currentPath:
                        self.moveProgress.y = 45
                    elif math.floor(self.position + 100) == self.currentPath:
                        self.moveProgress.y = -45
                else:
                    self.move(playerView)
    
    def move(self, view):
        if self.moveProgress.x > 0:
            if self.moveProgress.x - 3 > 0:
                velocity = pygame.math.Vector2(3, 0)
                self.moveProgress.x -= 3
            else:
                velocity = pygame.math.Vector2(3 - self.moveProgress.x, 0)
                self.moveProgress.x = 0
            self.rotate('right')
        elif self.moveProgress.x < 0:
            if self.moveProgress.x + 3 < 0:
                velocity = pygame.math.Vector2(-3, 0)
                self.moveProgress.x += 3
            else:
                velocity = pygame.math.Vector2(3 + self.moveProgress.x, 0)
                self.moveProgress.x += 3
            self.rotate('left')
        elif self.moveProgress.y > 0:
            if self.moveProgress.y - 3 > 0:
                velocity = pygame.math.Vector2(0, -3)
                self.moveProgress.y -= 3
            else:
                velocity = pygame.math.Vector2(3 - self.moveProgress.y, 0)
                self.moveProgress.y = 0
            self.rotate('up')
        elif self.moveProgress.y < 0:
            if self.moveProgress.y + 3 < 0:
                velocity = pygame.math.Vector2(0, 3)
                self.moveProgress.y += 3
            else:
                velocity = pygame.math.Vector2(3 + self.moveProgress.y, 0)
                self.moveProgress.y = 0
            self.rotate('down')
        self.pos += velocity
        self.relPos = self.pos - view.cameraPos
        self.rect.topleft = self.pos
        
    def getDestination(self, goal):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))                
        destination = self.myMap.cordsConversion(math.floor(goal.x/42), math.floor(goal.y/42))                     
        self.path = self.myMap.shortestPath(self.position, destination)
        
    def rotate(self, direction):
        difference = 0
        if direction == 'left':
            if self.angle != 180:
                difference = (180 - self.angle) % 360
                self.angle = 180
        elif direction == 'right':
            if self.angle != 0:
                difference = (360 - self.angle) % 360
                self.angle = 0
        elif direction == 'up':
            if self.angle != 90:
                difference = (90 - self.angle) % 360
                self.angle = 90
        elif direction == 'down':
            if self.angle != 270:
                difference = (270 - self.angle) % 360
                self.angle = 270
        self.image = self.rotateHelper(self.image, difference)
        
    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

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
