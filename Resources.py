import pygame
import math
import ItemList

class Tree(pygame.sprite.Sprite):
    def __init__(self, myMap, playerView, location, layer, group):
        self.myMap = myMap
        self.group = group
        self._layer = layer
        self.playerView = playerView
        self.image = pygame.image.load('img/Tree.png').convert_alpha()
        self.leaf = pygame.image.load('img/Leaf.png').convert_alpha()
        self.temp = pygame.Surface((self.leaf.get_width(), self.leaf.get_height())).convert()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = None
        pygame.sprite.Sprite.__init__(self, group)
        
    def update(self):
        self.rect.x = self.pos.x + self.playerView.cameraPos.x
        self.rect.y = self.pos.y + self.playerView.cameraPos.y
        itemGenerator = ItemList.itemList(self.group)
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
        if self.destroy:
            self.myMap.entityList.remove(self)
            self.myMap.addEdgesFrom(self.position, 'all')
            self.myMap.entityList.append(Trunk(self.myMap, (self.pos.x, self.pos.y)))
            if self.destroy == "south":
                self.myMap.entityList.append(itemGenerator.createItem("Log", self.myMap, self.pos.x, self.pos.y + 42, 'down'))
            elif self.destroy == "north":
                self.myMap.entityList.append(itemGenerator.createItem("Log", self.myMap, self.pos.x, self.pos.y - (42*5), 'up'))
            elif self.destroy == "east":
                self.myMap.entityList.append(itemGenerator.createItem("Log", self.myMap, self.pos.x+42, self.pos.y, 'right'))
            if self.destroy == "west":
                self.myMap.entityList.append(itemGenerator.createItem("Log", self.myMap, self.pos.x-(42*5), self.pos.y, 'left'))

    def draw_self(self, window, playerView):
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+playerView.cameraPos.x, self.pos.y+playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

class Trunk():
    def __init__(self, myMap, location):
        pygame.sprite.Sprite.__init__(self)
        self.myMap = myMap
        self.image = pygame.image.load('img/Tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = False
        
    def update(self):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
        if self.destroy:
            self.myMap.entityList.remove(self)
            self.myMap.addEdgesFrom(self.position, 'all')
    
    def draw_self(self, window, playerView):
        window.blit(self.image, self.pos+playerView.cameraPos)            
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+playerView.cameraPos.x, self.pos.y+playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

class Wall(pygame.sprite.Sprite):
    def __init__(self, name, imgName, myMap, playerView, location, getWeight, getWidth, getHeight, direction, layer, group):
        self._layer = layer
        self.myMap = myMap
        self.angle = 0
        self.playerView = playerView
        self.image = pygame.image.load(imgName).convert_alpha()
        self.weight = getWeight
        self.width = getWidth
        self.height = getHeight
        self.carryWeight = 0
        self.pos = pygame.math.Vector2(location)
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x)/42), math.floor((self.pos.y)/42))
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.destroy = False
        self.rect = self.image.get_rect(topleft=location)
        if direction == 'left':
            self.rotate(90)
            self.rotate(90)            
        elif direction == 'right':
            self.rect.height = 42*self.height
            self.rect.width = 42*self.width
        elif direction == 'up':
            self.rotate(90)
        elif direction == 'down':
            self.rotate(-90)
        self.updateEdges('remove')
        pygame.sprite.Sprite.__init__(self, group)

    def update(self):
        self.rect.x = self.pos.x + self.playerView.cameraPos.x
        self.rect.y = self.pos.y + self.playerView.cameraPos.y
        if self.destroy:
            self.myMap.entityList.remove(self)
            self.updateEdges('add')
                
    def updateEdges(self, modify):
        if modify == 'add':
            self.myMap.addEdgesFrom(self.position, 'all')
        elif modify == 'remove':
            self.myMap.removeEdgesFrom(self.position, 'into')

    def draw_self(self, window, playerView):
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+self.playerView.cameraPos.x, self.pos.y+self.playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

    #change this rotation to be similar to players
    def rotate(self, amount = 90):
        self.angle = (self.angle + amount)%360
        if self.angle == 0 or self.angle == 180:
            self.rect.height = 42*(self.height)
            self.rect.width = 42*(self.width)
        elif self.angle == 90 or self.angle == 270:
            self.rect.height = 42*self.width
            self.rect.width = 42*self.height
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y 
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x)/42), math.floor((self.pos.y)/42))
        self.image = self.rotateHelper(self.image, amount)

    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class Item(pygame.sprite.Sprite):
    def __init__(self, name, imgName, myMap, playerView, location, getWeight, getWidth, getHeight, direction, layer, group):
        self._layer = layer
        self.myMap = myMap
        self.angle = 0
        self.playerView = playerView
        self.image = pygame.image.load(imgName).convert_alpha()
        self.weight = getWeight
        self.width = getWidth
        self.height = getHeight
        self.name = name
        self.carryWeight = 0
        self.pos = pygame.math.Vector2(location)
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x)/42), math.floor((self.pos.y)/42))
        self.maxDurability = 100
        self.durability = self.maxDurability
        self.destroy = False
        self.rect = self.image.get_rect(topleft=location)
        if direction == 'left':
            self.rotate(90)
            self.rotate(90)            
        elif direction == 'right':
            self.rect.height = 42*self.height
            self.rect.width = 42*self.width
        elif direction == 'up':
            self.rotate(90)
        elif direction == 'down':
            self.rotate(-90)
        pygame.sprite.Sprite.__init__(self, group)

    def update(self):
        self.rect.x = self.pos.x + self.playerView.cameraPos.x
        self.rect.y = self.pos.y + self.playerView.cameraPos.y
        if self.destroy:
            self.myMap.entityList.remove(self)
            self.updateEdges('add')
                
    def updateEdges(self, modify):
        if modify == 'add':
            self.myMap.addEdgesFrom(self.position, 'all')
        elif modify == 'remove':
            self.myMap.removeEdgesFrom(self.position, 'into')

    def draw_self(self, window, playerView):
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+self.playerView.cameraPos.x, self.pos.y+self.playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

    def rotate(self, amount = 90):
        self.angle = (self.angle + amount)%360
        if self.angle == 0 or self.angle == 180:
            self.rect.height = 42*(self.height)
            self.rect.width = 42*(self.width)
        elif self.angle == 90 or self.angle == 270:
            self.rect.height = 42*self.width
            self.rect.width = 42*self.height
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y 
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x)/42), math.floor((self.pos.y)/42))
        self.image = self.rotateHelper(self.image, amount)

    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image
