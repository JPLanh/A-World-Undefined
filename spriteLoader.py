import pygame

class spriteLoader(pygame.sprite.Sprite):
  def __init__(self, spriteSheet):
    self.spriteSheet = pygame.image.load(spriteSheet)

  def getImage(self, x, y, width, height):
    image = pygame.Surface([width, height])
    image.blit(self.spriteSheet, (0, 0), (x, y, width, height))
    image.set_colorkey((0,0,0))
    return image

    
  
    
