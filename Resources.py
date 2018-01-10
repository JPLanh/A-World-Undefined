import pygame
import math

class Tree():
    def __init__(self, myMap, location, playerView):
        self.myMap = myMap
        self.image = pygame.image.load('img/Tree.png').convert_alpha()
        self.leaf = pygame.image.load('img/Leaf.png').convert_alpha()
        self.temp = pygame.Surface((self.leaf.get_width(), self.leaf.get_height())).convert()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = None
        
    def update(self, playerView, entityList):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
        if self.destroy:
            entityList.remove(self)
            self.myMap.addEdgesFrom(self.position, 'all')
            entityList.append(Trunk(self.myMap, (self.pos.x, self.pos.y), playerView))
            if self.destroy == "south":
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y + 42), playerView, 'down'))        
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y + 42*2), playerView, 'down')) 
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y + 42*3), playerView, 'down'))         
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y + 42*4), playerView, 'down'))         
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y + 42*5), playerView, 'down'))         
            elif self.destroy == "north":
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y - 42), playerView, 'down'))        
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y - 42*2), playerView, 'down')) 
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y - 42*3), playerView, 'down')) 
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y - 42*4), playerView, 'down')) 
                entityList.append(Log(self.myMap, (self.pos.x, self.pos.y - 42*5), playerView, 'down'))
            elif self.destroy == "east":
                entityList.append(Log(self.myMap, (self.pos.x+42, self.pos.y), playerView, 'right'))        
                entityList.append(Log(self.myMap, (self.pos.x+42*2, self.pos.y), playerView, 'right')) 
                entityList.append(Log(self.myMap, (self.pos.x+42*3, self.pos.y), playerView, 'right')) 
                entityList.append(Log(self.myMap, (self.pos.x+42*4, self.pos.y), playerView, 'right')) 
                entityList.append(Log(self.myMap, (self.pos.x+42*5, self.pos.y), playerView, 'right'))         
            if self.destroy == "west":
                entityList.append(Log(self.myMap, (self.pos.x-42, self.pos.y), playerView, 'left'))       
                entityList.append(Log(self.myMap, (self.pos.x-42*2, self.pos.y), playerView, 'left')) 
                entityList.append(Log(self.myMap, (self.pos.x-42*3, self.pos.y), playerView, 'left')) 
                entityList.append(Log(self.myMap, (self.pos.x-42*4, self.pos.y), playerView, 'left')) 
                entityList.append(Log(self.myMap, (self.pos.x-42*5, self.pos.y), playerView, 'left'))                  
    
    def draw_self(self, window, playerView):
        #if not self.destroy:
        window.blit(self.image, self.pos+playerView.cameraPos)
        self.temp.blit(window, -(self.pos+playerView.cameraPos+(-self.image.get_width()/2, -self.image.get_height()/2)))
        self.temp.blit(self.leaf, (0, 0))
        self.temp.set_alpha(210)            
        window.blit(self.temp, self.pos+playerView.cameraPos+(-self.image.get_width()/2, -self.image.get_height()/2))
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+playerView.cameraPos.x, self.pos.y+playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

class Trunk():
    def __init__(self, myMap, location, playerView):
        self.myMap = myMap
        self.image = pygame.image.load('img/Tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = False
        
    def update(self, playerView, entityList):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
        if self.destroy:
            entityList.remove(self)
            self.myMap.addEdgesFrom(self.position, 'all')
    
    def draw_self(self, window, playerView):
        window.blit(self.image, self.pos+playerView.cameraPos)            
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+playerView.cameraPos.x, self.pos.y+playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)
            
class Log():
    def __init__(self, myMap, location, playerView, direction):
        self.myMap = myMap
        self.angle = 270
        self.direction = direction
        self.image = pygame.image.load('img/Log.png').convert_alpha()
        self.rotate()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = False
        
    def update(self, playerView, entityList):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
        if self.destroy:
            entityList.remove(self)
            self.myMap.addEdgesFrom(self.position, 'all')        
    
    def draw_self(self, window, playerView):
        window.blit(self.image, self.pos+playerView.cameraPos)            
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+playerView.cameraPos.x, self.pos.y+playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

    def rotate(self):
        difference = 0
        if self.direction == 'left':
            if self.angle != 180:
                difference = (180 - self.angle) % 360
                self.angle = 180
        elif self.direction == 'right':
            if self.angle != 0:
                difference = (360 - self.angle) % 360
                self.angle = 0
        elif self.direction == 'up':
            if self.angle != 90:
                difference = (90 - self.angle) % 360
                self.angle = 90
        elif self.direction == 'down':
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
