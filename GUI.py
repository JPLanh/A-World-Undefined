import pygame

import menu
import spriteLoader

class Frame:
    def __init__(self, window, width, height, layer, playerView = None):
        loadSprites = spriteLoader.spriteLoader('img/Frame/menuSpriteSheet.png')
        self.playerView = playerView
        self.topLeft = menu.topLeftMenu(layer, (0, 0), playerView) 
        self.top = menu.topMenu(layer, (42, 0), playerView) 
        self.topRight = menu.topRightMenu(layer, (84, 0), playerView) 
##        self.CORNER = pygame.image.load('img/Frame/guiTopLeft.png').convert_alpha()
##        self.SIDE = pygame.image.load('img/Frame/guiLeft.png').convert_alpha()
##        self.CENTER = pygame.image.load('img/Frame/guiMid.png').convert_alpha()
        self.surface = pygame.Surface((width*42, height*42))
        self.window = window
        self.width = width
        self.height = height

##    def displayFrame(self, xGet, yGet):
##        self.surface.blit(self.CORNER, (0,0))
##        self.CORNER = self.rotateHelper(self.CORNER, 90)
##        self.surface.blit(self.CORNER, (0 , (self.height-1)*42))
##        self.CORNER = self.rotateHelper(self.CORNER, 90)
##        self.surface.blit(self.CORNER, ((self.width-1)*42, (self.height-1)*42))
##        self.CORNER = self.rotateHelper(self.CORNER, 90)
##        self.surface.blit(self.CORNER, ((self.width-1)*42,0))
##        self.CORNER = self.rotateHelper(self.CORNER, 90)
##
##        if(self.height > 2):
##            for y in range(1, self.height-1):
##                self.surface.blit(self.SIDE, (0, y*42))
##        self.SIDE = self.rotateHelper(self.SIDE, 90)            
##        if(self.width > 2):
##            for x in range(1, self.width-1):
##                self.surface.blit(self.SIDE, (x*42, (self.height-1)*42))
##        self.SIDE = self.rotateHelper(self.SIDE, 90)  
##        if(self.height > 2):
##            for y in range(1, self.height-1):
##                self.surface.blit(self.SIDE, ((self.width-1)*42, y*42))
##        self.SIDE = self.rotateHelper(self.SIDE, 90)            
##        if(self.width > 2):
##            for x in range(1, self.width-1):
##                self.surface.blit(self.SIDE, (x*42, 0))
##        self.SIDE = self.rotateHelper(self.SIDE, 90)
##
##        if (self.width > 2 and self.height > 2):
##            for x in range(1, self.width-1):
##                for y in range(1, self.height-1):
##                    self.surface.blit(self.CENTER, (x*42, y*42))
##
##        if self.playerView == None:
##            self.window.blit(self.surface, (xGet, yGet))
##        else:
##            self.window.blit(self.surface, (xGet+self.playerView.cameraPos.x, yGet+self.playerView.cameraPos.y))
            
    def rotateHelper(self, image, angle):
        original_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = original_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

class TextField(pygame.sprite.Sprite):
    def __init__(self, window, layer, playerView = None):
        self.playerView = playerView
        self._layer = layer
        self.window = window
        self.largeText = pygame.font.SysFont("aerial", 18)
        pygame.sprite.Sprite.__init__(self)

    def displayMessage(self, text, xPos, yPos):
        TextSurf, TextRect = self.text_object(text, self.largeText)
        if self.playerView == None:
            TextRect.center = (xPos, yPos)
        else:
            TextRect.center = (xPos+self.playerView.cameraPos.x, yPos+self.playerView.cameraPos.y)
        self.window.blit(TextSurf, TextRect)
            
    def text_object(self, text, font):
        #third paramset set color
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()
