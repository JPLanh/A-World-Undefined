import pygame
import GUI

class Camera:

  CORNER = None;
  SIDE = None;
  CENTER = None;
  ITEMSLOT = None;
  
  def __init__(self, window):
    self.window = window
    self.cameraPos = pygame.math.Vector2(0, 0)
    self.focusPlayer = None
    self.vel = pygame.math.Vector2(0, 0)
    self.focusGUI = pygame.Surface((4*42,6*42), pygame.SRCALPHA, 32)
    self.focusGUI = self.focusGUI.convert_alpha()
    self.menuGUI = GUI.Frame(window, 4, 6, 200)
    self.optionGUI = GUI.Frame(window, 2, 4, 99, self)
    self.optionGUIText = GUI.TextField(window, 100, self)
    self.zonePosition = None
    self.zoneAction = None
    self.xMouse = None
    self.yMouse = None
    self.ITEMSLOT = pygame.image.load('img/Frame/Equip.png').convert_alpha()

  def zoneMenu(self, getPosition, xMouse, yMouse):
    self.zonePosition = getPosition
    self.xMouse = xMouse
    self.yMouse = yMouse
    
  def update(self):
    self.cameraPos += self.vel
    if self.focusPlayer:
      self.menuGUI.displayFrame(0, 0)
      for x in self.focusPlayer.Body:
        self.focusGUI.blit(pygame.image.load('img/Frame/Equip.png').convert_alpha(), (self.focusPlayer.Body[x].pos.x, self.focusPlayer.Body[x].pos.y))
        if self.focusPlayer.Body[x].item:
          self.focusGUI.blit(self.focusPlayer.Body[x].item.image, (self.focusPlayer.Body[x].pos.x-6, self.focusPlayer.Body[x].pos.y-6))
        else:
          None
      if self.zonePosition:
        self.optionGUI.displayFrame(self.xMouse, self.yMouse)
        for i in self.zoneAction:
          self.optionGUIText.displayMessage(i, self.xMouse+40, (self.yMouse+15) + (20*self.zoneAction.index(i)))
#      self.message_display(self.focusPlayer.name, self.window)
      self.window.blit(self.focusGUI, (0, 0))
                
  def rotateHelper(self, image, angle):
      original_rect = image.get_rect()
      rot_image = pygame.transform.rotate(image, angle)
      rot_rect = original_rect.copy()
      rot_rect.center = rot_image.get_rect().center
      rot_image = rot_image.subsurface(rot_rect).copy()
      return rot_image
