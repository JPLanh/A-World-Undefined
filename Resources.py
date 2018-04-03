import pygame
import constant
import math
import ItemList
import Entity

class HarvestableNode(Entity.Entity):
    def __init__(self, name, mapGet, playerView, location, angle, layer):
        Entity.Entity.__init__(self, name, "img/Bark.png", mapGet, playerView, 270, location, layer)
        print(self.position)

    def update(self):
        self.rect.x = (self.coordinate.x + self.playerView.cameraPos.x) + (self.coordinate.y + self.playerView.cameraPos.y)/18
        self.rect.y = self.coordinate.y + self.playerView.cameraPos.y
        self.myMap.removeEdgesFrom(self.position, 'into')
                       
class NonHarvestableNode(Entity.Entity):
    def __init__(self, name, mapGet, playerView, location, angle, layer):
        Entity.Entity.__init__(self, name, "img/Leaf.png", mapGet, playerView, 270, location, layer)

    def update(self):
        self.rect.x = (self.coordinate.x + self.playerView.cameraPos.x) + (self.coordinate.y + self.playerView.cameraPos.y)/18
        self.rect.y = self.coordinate.y + self.playerView.cameraPos.y - 48
        self.myMap.removeEdgesFrom(self.position, 'into')
                       
class Wall(Entity.Entity):
    def __init__(self, name, mapGet, playerView, location, angle, layer):
        Entity.Entity.__init__(self, name, "img/"+name+".png", mapGet, playerView, 270, location, layer)
        self.maxDurability = 100
        self.myMap.removeEdgesFrom(self.position, 'into')
        self.durability = self.maxDurability

    def update(self):
        self.rect.x = (self.coordinate.x + self.playerView.cameraPos.x) + (self.coordinate.y + self.playerView.cameraPos.y)/18 - 12
        self.rect.y = self.coordinate.y + self.playerView.cameraPos.y - 42
        self.myMap.removeEdgesFrom(self.position, 'into')
                
    def draw_self(self, window, playerView):
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+self.playerView.cameraPos.x, self.pos.y+self.playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class Item(Entity.Entity):
    def __init__(self, name, imgName, mapGet, playerView, location, angle, layer):
        Entity.Entity.__init__(self, name, imgName, mapGet, playerView, 270, location, layer)
        self.maxDurability = 100
        self.durability = self.maxDurability
        if angle == 180:
            self.image = self.rotateHelper(self.image, 90)
            self.image = self.rotateHelper(self.image, 90)
        elif angle == 90:
            self.image = self.rotateHelper(self.image, 90)
        elif angle == 270:
            self.image = self.rotateHelper(self.image, -90)

    def update(self):
        self.rect.x = self.pos.x + self.playerView.cameraPos.x
        self.rect.y = self.pos.y + self.playerView.cameraPos.y
                
    def draw_self(self, window, playerView):
        if self.durability < self.maxDurability:
          pygame.draw.rect(window, (0, 0, 0), (self.pos.x+self.playerView.cameraPos.x, self.pos.y+self.playerView.cameraPos.y+21, 42*(self.durability/self.maxDurability), 10), 1)

    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class Floor(Entity.Entity):
    def __init__(self, name, imgName, mapGet, playerView, location, angle, layer):
        Entity.Entity.__init__(self, name, imgName, mapGet, playerView, 270, location, layer)
