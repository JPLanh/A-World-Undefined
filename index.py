
import pygame
import math
import time

import node
import mapGenerator
import Person
import Camera
import Resources
import ItemList

FRAME_WIDTH = 800
FRAME_HEIGHT = 600
TILE_SIZE = 42
TILE_WIDTH = math.floor(FRAME_WIDTH / TILE_SIZE)
TILE_HEIGHT = math.floor(FRAME_HEIGHT / TILE_SIZE)
MAX_X_TILES = 100
MAX_Y_TILES = 100

pygame.init()

mapOne = node.Graph(MAX_X_TILES,MAX_Y_TILES)
BACKGROUND = mapGenerator.initialize(TILE_SIZE)

gameDisplay = pygame.display.set_mode((TILE_WIDTH*TILE_SIZE,TILE_HEIGHT*TILE_SIZE))
pygame.display.set_caption('A simulation')
playerView = Camera.Camera(gameDisplay)
clock = pygame.time.Clock()

itemGenerator = ItemList.itemList()

mapOne.entityList.append(Person.Person('Jimmy', mapOne, (42*6-3, 42*4-3), playerView))
#mapOne.entityList.append(Person.Person('Yurika', mapOne, (42*12-3, 42*8-3), playerView))
mapOne.entityList.append(Resources.Tree(mapOne, (42*12, 42*12)))
mapOne.entityList.append(Resources.Tree(mapOne, (42*12, 42*13)))
mapOne.entityList.append(Resources.Tree(mapOne, (42*13, 42*13)))
mapOne.entityList.append(Resources.Tree(mapOne, (42*12, 42*11)))
mapOne.entityList.append(itemGenerator.createItem("Log", mapOne, 42*8, 42*7, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*5, 42*0, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*10, 42*0, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*15, 42*0, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*5, 42*0, 'down'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*19, 42*0, 'down'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*5, 42*5, 'down'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*19, 42*5, 'down'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*5, 42*9, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*8, 42*9, 'left'))
mapOne.entityList.append(itemGenerator.createWall("Lumber", mapOne, 42*15, 42*9, 'left'))
mapOne.entityList.append(itemGenerator.createItem("Saw", mapOne, 42*6, 42*5, 'left'))


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
  gameDisplay.blit(BACKGROUND, (0, 0)+playerView.cameraPos)
  for entities in mapOne.entityList:
    entities.update()
    entities.draw_self(gameDisplay, playerView)
  playerView.update()
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
        
        if event.key == pygame.K_ESCAPE:
          playerView.focusPlayer = None
          
        if event.key == pygame.K_j:
          #drop
            print("Dropping")
            if playerView.focusPlayer:
              if playerView.focusPlayer.Body['Left Hand'].item == playerView.focusPlayer.Body['Right Hand'].item:
                playerView.focusPlayer.dropItem("Both")
              else:
                playerView.focusPlayer.dropItem("Right Hand")
                
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
          for player in mapOne.entityList:
            playerX, playerY, playerWidth, playerHeight = player.rect
            if mouseX > playerX+cameraX and mouseX < playerX+playerWidth+cameraX:
              if mouseY > playerY+cameraY and mouseY < playerY+playerHeight+cameraY:
                if isinstance(player, Person.Person):
                  playerView.focusPlayer = player

        elif event.button == 3:
          if playerView.focusPlayer:
            playerView.focusPlayer.stopAction()
            movable = True
            #selectedEntities = getClicks(mouseX, mouseY, cameraX, cameraY)
            #if selectedEntities:
       #implement some sort of way to focus             
            for player in mapOne.entityList:
              playerX, playerY, playerWidth, playerHeight = player.rect
              if mouseX > playerX+cameraX and mouseX < playerX+playerWidth+cameraX:
                if mouseY > playerY+cameraY and mouseY < playerY+playerHeight+cameraY:
                  movable = False
                  if playerView.focusPlayer == player:
                    playerView.focusPlayer.action()
                  else:
                    playerView.focusPlayer.newOrders = pygame.math.Vector2(mouseX-cameraX, mouseY-cameraY)
                    playerView.focusPlayer.focusTarget = player
            if movable:
              playerView.focusPlayer.newOrders = pygame.math.Vector2(mouseX-cameraX, mouseY-cameraY)
    updates()

#implement searching for entity at a spot
def getClicks(mouseX, mouseY, cameraX, cameraY):
  selectedEntity = []
  for player in mapOne.entityList:
    playerX, playerY, playerWidth, playerHeight = player.rect
    if mouseX > playerX+cameraX and mouseX < playerX+playerWidth+cameraX:
      if mouseY > playerY+cameraY and mouseY < playerY+playerHeight+cameraY:
        selectedEntity.add(player)
  return selectedEntity

game_loop()
pygame.quit()
quit()
