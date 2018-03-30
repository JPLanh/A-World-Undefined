import pygame

class spriteLoader(pygame.sprite.Sprite):
  def __init__(self, spriteSheet):
    self.spriteSheet = pygame.image.load(spriteSheet)

  def getImage(self, x, y, width, height):
    image = pygame.Surface([60, 60])
    image.blit(self.spriteSheet, (0, 0), (x, y, 60, 60))
    image.set_colorkey((0,0,0))
    return image

  def personLoader():
    return pygame.image.load('img/Bot.png').convert_alpha()
