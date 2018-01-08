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
        self.durability = 100
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = False
        
    def update(self, playerView):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
    
    def draw_self(self, window, playerView):
        if not self.destroy:
            window.blit(self.image, self.pos+playerView.cameraPos)
            self.temp.blit(window, -(self.pos+playerView.cameraPos+(-self.image.get_width()/2, -self.image.get_height()/2)))
            self.temp.blit(self.leaf, (0, 0))
            self.temp.set_alpha(210)            
            window.blit(self.temp, self.pos+playerView.cameraPos+(-self.image.get_width()/2, -self.image.get_height()/2))

class Log():
    def __init__(self, myMap, location, playerView):
        self.myMap = myMap
        self.image = pygame.image.load('img/Bot.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.durability = 100
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)
        self.destroy = False
        
    def update(self, playerView):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
    
    def draw_self(self, window, playerView):
        if not self.destroy:
            window.blit(self.image, self.pos+playerView.cameraPos)
