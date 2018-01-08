import pygame
import math
import time

import node
import mapGenerator
import Person
import Camera
import Resources

FRAME_WIDTH = 800
FRAME_HEIGHT = 600
TILE_SIZE = 42
TILE_WIDTH = math.floor(FRAME_WIDTH / TILE_SIZE)
TILE_HEIGHT = math.floor(FRAME_HEIGHT / TILE_SIZE)

pygame.init()

mapOne = node.Graph(100,100)
BACKGROUND = mapGenerator.initialize(TILE_SIZE)
allEntity = []

gameDisplay = pygame.display.set_mode((TILE_WIDTH*TILE_SIZE,TILE_HEIGHT*TILE_SIZE))
pygame.display.set_caption('A simulation')

playerView = Camera.Camera()
allEntity.append(Person.Person('Jimmy', mapOne, (42*5-3, 42*5-3), playerView))
allEntity.append(Person.Person('Yurika', mapOne, (42*8-3, 42*5-3), playerView))
allEntity.append(Resources.Tree(mapOne, (42*7, 42*7), playerView))

clock = pygame.time.Clock()

def text():
  message_display('pow')

def text_object(text, font):
  #third paramset set color
  textSurface = font.render(text, True, BLACK)
  return textSurface, textSurface.get_rect()

def message_display(text):
  largeText = pygame.font.Font('freesansbold.ttf', 115)
  TextSurf, TextRect = text_object(text, largeText)
  TextRect.center = ((FRAME_WIDTH/2), (FRAME_HEIGHT/2))
  gameDisplay.blit(TextSurf, TextRect)

  pygame.display.update()
  time.sleep(2)

def updates():
  playerView.update()
  gameDisplay.blit(BACKGROUND, (0, 0)+playerView.cameraPos)
  for entities in allEntity:
    if entities.destroy:
      if isinstance(entities, Resources.Tree):
        allEntity.append(Resources.Log(mapOne, (entities.pos.x, entities.pos.y), playerView))        
        allEntity.remove(entities)
    entities.update(playerView)
    entities.draw_self(gameDisplay, playerView)
  pygame.display.flip()

  #fps configuration
  clock.tick(30)

def game_loop():

  start = False

  while not start:
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        start = True
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_j:
          print(mapOne.checkEnterable(707))
            
        if event.key == pygame.K_a:
            playerView.vel.x = +10
        if event.key == pygame.K_d:
            playerView.vel.x = -10
        if event.key == pygame.K_s:
            playerView.vel.y = -10
        if event.key == pygame.K_w:
            playerView.vel.y = +10

      elif event.type == pygame.KEYUP:
        if event.key in (pygame.K_a, pygame.K_d):
          playerView.vel.x = 0
        elif event.key in (pygame.K_w, pygame.K_s):
          playerView.vel.y = 0

      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouseX, mouseY = pygame.mouse.get_pos()
        cameraX, cameraY = playerView.cameraPos
        if event.button == 1:
          for player in allEntity:
            playerX, playerY, playerWidth, playerHeight = player.rect
            if mouseX > playerX+cameraX and mouseX < playerX+playerWidth+cameraX:
              if mouseY > playerY+cameraY and mouseY < playerY+playerHeight+cameraY:
                if isinstance(player, Person.Person):
                  playerView.focusPlayer = player
        elif event.button == 3:
          if playerView.focusPlayer:
            playerView.focusPlayer.stopAction()
            movable = True
            for player in allEntity:
              playerX, playerY, playerWidth, playerHeight = player.rect
              if mouseX > playerX+cameraX and mouseX < playerX+playerWidth+cameraX:
                if mouseY > playerY+cameraY and mouseY < playerY+playerHeight+cameraY:
                  movable = False
                  if isinstance(player, Person.Person):
                    print("move to a person")
                  elif isinstance(player, Resources.Tree):
                    playerView.focusPlayer.newOrders = pygame.math.Vector2(mouseX-cameraX, mouseY-cameraY)
                    playerView.focusPlayer.harvesting = player
                    print("harvest tree")
            if movable:
              playerView.focusPlayer.newOrders = pygame.math.Vector2(mouseX-cameraX, mouseY-cameraY)

#      elif event.type == pygame.MOUSEBUTTONUP:
#        mouseX, mouseY = pygame.mouse.get_pos()
#        if menuGui.active:
          #FIX HERE, so far it's a cross shape of a nono-section due to the next two statement
#          if mouseX < playerX+cameraX or mouseX > playerX+playerWidth+cameraX:
#              if mouseY < playerY+cameraY or mouseY > playerY+playerHeight+cameraY:
#                if mouseX > 400 and mouseY < 300:
#                  playerView.focusPlayer.moving = True
#                if mouseX < 400 and mouseY < 300:
#                  print("Quad II")
#                if mouseX < 400 and mouseY > 300:
#                  print("Quad III")
#                if mouseX > 400 and mouseY > 300:
#                  print("Quad IV")
#        menuGui.active = False

    updates()

game_loop()
pygame.quit()
quit()
