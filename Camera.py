import pygame

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
    self.generateFocusGUI()
    self.CORNER = pygame.image.load('img/Frame/guiTopLeft.png').convert_alpha()
    self.SIDE = pygame.image.load('img/Frame/guiLeft.png').convert_alpha()
    self.CENTER = pygame.image.load('img/Frame/guiMid.png').convert_alpha()

    self.ITEMSLOT = pygame.image.load('img/Frame/Equip.png').convert_alpha()
    
  def generateFocusGUI(self):
    self.focusGUI = pygame.Surface((4*42,6*42))
    
  def text_object(self, text, font):
    #third paramset set color
    textSurface = font.render(text, True, (0, 0, 0))
    return textSurface, textSurface.get_rect()

  def message_display(self, text, window):
    largeText = pygame.font.Font('freesansbold.ttf', 12)
    TextSurf, TextRect = self.text_object(text, largeText)
    TextRect.center = (42, 5)
    window.blit(TextSurf, TextRect)
        
  def update(self):
    self.cameraPos += self.vel
    if self.focusPlayer:
      self.focusGUI.blit(self.CORNER, (0, 0))
      self.CORNER = self.rotateHelper(self.CORNER, 90)
      self.focusGUI.blit(self.CORNER, (0, 210))
      self.CORNER = self.rotateHelper(self.CORNER, 90)
      self.focusGUI.blit(self.CORNER, (126, 210))
      self.CORNER = self.rotateHelper(self.CORNER, 90)
      self.focusGUI.blit(self.CORNER, (126, 0))
      self.CORNER = self.rotateHelper(self.CORNER, 90)

      self.focusGUI.blit(self.SIDE, (0, 42))
      self.focusGUI.blit(self.SIDE, (0, 84))
      self.focusGUI.blit(self.SIDE, (0, 126))
      self.focusGUI.blit(self.SIDE, (0, 168))
      self.SIDE = self.rotateHelper(self.SIDE, 90)
      self.focusGUI.blit(self.SIDE, (42, 210))
      self.focusGUI.blit(self.SIDE, (84, 210))
      self.SIDE = self.rotateHelper(self.SIDE, 90)
      self.focusGUI.blit(self.SIDE, (126, 42))
      self.focusGUI.blit(self.SIDE, (126, 84))
      self.focusGUI.blit(self.SIDE, (126, 126))
      self.focusGUI.blit(self.SIDE, (126, 168))
      self.SIDE = self.rotateHelper(self.SIDE, 90)
      self.focusGUI.blit(self.SIDE, (42, 0))
      self.focusGUI.blit(self.SIDE, (84, 0))
      self.focusGUI.blit(self.CENTER, (42, 42))
      self.focusGUI.blit(self.CENTER, (84, 42))
      self.focusGUI.blit(self.CENTER, (42, 84))
      self.focusGUI.blit(self.CENTER, (84, 84))
      self.focusGUI.blit(self.CENTER, (42, 126))
      self.focusGUI.blit(self.CENTER, (84, 126))
      self.focusGUI.blit(self.CENTER, (42, 168))
      self.focusGUI.blit(self.CENTER, (84, 168))
      self.SIDE = self.rotateHelper(self.SIDE, 90)
      for x in self.focusPlayer.Body:
        self.focusGUI.blit(pygame.image.load('img/Frame/Equip.png').convert_alpha(), (self.focusPlayer.Body[x].pos.x, self.focusPlayer.Body[x].pos.y))
        if self.focusPlayer.Body[x].item:
          self.focusGUI.blit(self.focusPlayer.Body[x].item.image, (self.focusPlayer.Body[x].pos.x-6, self.focusPlayer.Body[x].pos.y-6))
        else:
          None
      self.message_display(self.focusPlayer.name, self.window)
      self.window.blit(self.focusGUI, (0, 0))
                
  def rotateHelper(self, image, angle):
      original_rect = image.get_rect()
      rot_image = pygame.transform.rotate(image, angle)
      rot_rect = original_rect.copy()
      rot_rect.center = rot_image.get_rect().center
      rot_image = rot_image.subsurface(rot_rect).copy()
      return rot_image
