import pygame
import spriteLoader

class MenuSprite:
  def __init__(self, x, y):
    self.spriteSheet = spriteLoader.spriteLoader("img/Frame/menuSpriteSheet.png")
    self.image = self.spriteSheet.getImage(x, y, 42, 42)

class topMenu(pygame.sprite.Sprite):
  def __init__(self, layer, location, playerView = None):
    self.pos = pygame.math.Vector2(location)
    self._layer = layer
    self.playerView = playerView
    self.image = MenuSprite(42, 0).image
    self.rect = self.image.get_rect(topleft=location)
    pygame.sprite.Sprite.__init__(self)
    
  def update(self):
    self.rect.x = self.pos.x + self.playerView.cameraPos.x
    self.rect.y = self.pos.y + self.playerView.cameraPos.y

class topLeftMenu(pygame.sprite.Sprite):
  def __init__(self, layer, location, playerView = None):
    self.pos = pygame.math.Vector2(location)
    self._layer = layer
    self.playerView = playerView
    self.image = MenuSprite(0, 0).image
    self.rect = self.image.get_rect(topleft=location)
    pygame.sprite.Sprite.__init__(self)
    
  def update(self):
    self.rect.x = self.pos.x + self.playerView.cameraPos.x
    self.rect.y = self.pos.y + self.playerView.cameraPos.y

class topRightMenu(pygame.sprite.Sprite):
  def __init__(self, layer, location, playerView = None):
    self.pos = pygame.math.Vector2(location)
    self._layer = layer
    self.playerView = playerView
    self.image = MenuSprite(84, 0).image
    self.rect = self.image.get_rect(topleft=location)
    pygame.sprite.Sprite.__init__(self)
    
  def update(self):
    self.rect.x = self.pos.x + self.playerView.cameraPos.x
    self.rect.y = self.pos.y + self.playerView.cameraPos.y
