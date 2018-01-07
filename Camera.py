import pygame

class Camera:
  def __init__(self):
    self.cameraPos = pygame.math.Vector2(0, 0)
    self.focusPlayer = None
    self.vel = pygame.math.Vector2(0, 0)

  def update(self):
    self.cameraPos += self.vel
    
