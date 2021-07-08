import pygame

class TextField():
    def __init__(self):
        self.largeText = pygame.font.SysFont("aerial", 18)

    def displayMessage(self, text, xPos, yPos, window):
        TextSurf, TextRect = self.text_object(text, self.largeText)
        TextRect.center = (xPos, yPos)
        window.blit(TextSurf, TextRect)
            
    def text_object(self, text, font):
        #third paramset set color
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

class Debugger:
  def __init__(self):
    pygame.init()
    debuggerDisplay = pygame.display.set_mode((300, 500))
    test = TextField().displayMessage("Hello", 5, 5, debuggerDisplay)
