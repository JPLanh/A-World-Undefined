import pygame

class Menu:
  def __init__(self):
    self.active = False
    self.topLeftImage = pygame.image.load('img/Frame/topLeft.png').convert_alpha()
    self.topRightImage = pygame.image.load('img/Frame/topRight.png').convert_alpha()
    self.bottomLeftImage = pygame.image.load('img/Frame/bottomLeft.png').convert_alpha()
    self.bottomRightImage = pygame.image.load('img/Frame/bottomRight.png').convert_alpha()

  def update(self, centerPos):
    if self.active == True:
      self.tlRect = self.topLeftImage.get_rect(topleft=centerPos)
      self.trRect = self.topRightImage.get_rect(topleft=centerPos)
      self.blRect = self.bottomLeftImage.get_rect(topleft=centerPos)
      self.brRect = self.bottomRightImage.get_rect(topleft=centerPos)
      self.tlpos = pygame.math.Vector2(centerPos)
      self.trpos = pygame.math.Vector2(centerPos)
      self.blpos = pygame.math.Vector2(centerPos)
      self.brpos = pygame.math.Vector2(centerPos)
      self.val = pygame.math.Vector2(25, 25)
      self.brRect.topleft = self.brpos + self.val
      self.tlRect.topleft = self.tlpos - self.val
      self.val = pygame.math.Vector2(-25, 25)
      self.trRect.topleft = self.trpos - self.val
      self.blRect.topleft = self.blpos + self.val
    
  def draw_self(self, window):
    if self.active == True:
      window.blit(self.topLeftImage, self.tlRect)
      window.blit(self.topRightImage, self.trRect)
      window.blit(self.bottomLeftImage, self.blRect)
      window.blit(self.bottomRightImage, self.brRect)
