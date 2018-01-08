import pygame
import math

class Tree():
    def __init__(self, myMap, location, playerView):
        self.myMap = myMap
        self.image = pygame.image.load('img/Tree.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.pos = pygame.math.Vector2(location)
        self.durability = 100
        self.relPos = pygame.math.Vector2(location)-playerView.cameraPos
        self.position = self.myMap.cordsConversion(self.pos.x/42, self.pos.y/42)

    def harvested(self):
        del self.myMap
        del self.image
        del self.rect
        del self.pos
        del self.durability
        del self.relPos
        del self.position
        print("delete")
        
    def update(self, playerView):
        self.position = self.myMap.cordsConversion(math.floor((self.pos.x+3)/42), math.floor((self.pos.y+3)/42))
        self.myMap.removeEdgesFrom(self.position, 'into')
    
    def draw_self(self, window, playerView):
        window.blit(self.image, self.pos+playerView.cameraPos)
