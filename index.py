
import pygame
import math
import time

import node
import mapGenerator
import Person
import Camera
import Resources
import ItemList
import menu
import buildings

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
#choiceMenu = menu.Menu(gameDisplay, playerView)

entityGroup = pygame.sprite.LayeredUpdates()
outGroup = pygame.sprite.LayeredUpdates()

entitymover = None

itemGenerator = ItemList.itemList(entityGroup)

mapOne.entityList.append(Person.Person('Jimmy', mapOne, (42*6-3, 42*4-3), playerView, 25, entityGroup))
#mapOne.entityList.append(Person.Person('Yurika', mapOne, (42*12-3, 42*8-3), playerView))
mapOne.entityList.append(Resources.Tree(mapOne, playerView, (42*12, 42*12), 75, entityGroup))
mapOne.entityList.append(Resources.Tree(mapOne, playerView, (42*12, 42*13), 75, entityGroup))
mapOne.entityList.append(Resources.Tree(mapOne, playerView, (42*13, 42*13), 75, entityGroup))
mapOne.entityList.append(Resources.Tree(mapOne, playerView, (42*12, 42*11), 75, entityGroup))
mapOne.entityList.append(itemGenerator.createItem("Log", mapOne, playerView, 42*8, 42*7, 'left', 2))
buildings.Lumberyard(itemGenerator, mapOne, playerView, 5, 0, 10, 7)
mapOne.entityList.append(itemGenerator.createItem("Saw", mapOne, playerView, 42*6, 42*5, 'left', 7))


def updates():
  gameDisplay.blit(BACKGROUND, (0, 0)+playerView.cameraPos)
  entityGroup.update()
  entityGroup.draw(gameDisplay)
  outGroup.update()

  entitymover = None
  for i in entityGroup:
    if i.pos.x < -playerView.cameraPos.x or i.pos.x > -playerView.cameraPos.x + FRAME_WIDTH or i.pos.y < -playerView.cameraPos.y or i.pos.y > -playerView.cameraPos.y + FRAME_HEIGHT: 
        entitymover = i
  if entitymover != None:
    outGroup.add(entitymover)
    entityGroup.remove(entitymover)

  entitymover = None
  for i in outGroup:
    if i.pos.x >= -playerView.cameraPos.x and i.pos.x <= -playerView.cameraPos.x + FRAME_WIDTH:
      if i.pos.y >= -playerView.cameraPos.y and i.pos.y <= -playerView.cameraPos.y + FRAME_HEIGHT:
        entitymover = i
  if entitymover != None:
    entityGroup.add(entitymover)
    outGroup.remove(entitymover)
  playerView.update()
  #choiceMenu.update()
  pygame.display.flip()

  #fps configuration
  clock.tick(30)

clicks = 0
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
            if mouseX > playerX and mouseX < playerX+playerWidth:
              if mouseY > playerY and mouseY < playerY+playerHeight:
                if isinstance(player, Person.Person):
                  playerView.focusPlayer = player

        elif event.button == 3:
          if playerView.focusPlayer:
            playerView.focusPlayer.stopAction()
            movable = True
            playerView.zonePosition = None
            zoneAction = []
            zoneAction.append("Move")
            for player in mapOne.entityList:
              playerX, playerY, playerWidth, playerHeight = player.rect
              if mouseX > playerX and mouseX < playerX+playerWidth:
                if mouseY > playerY and mouseY < playerY+playerHeight:
                  movable = False
                  playerView.zoneMenu(mapOne.cordsConversion(mouseX, mouseY), mouseX, mouseY)
                  if playerView.focusPlayer == player:
                    playerView.focusPlayer.action()                
                  else:
                    playerView.focusPlayer.newOrders = pygame.math.Vector2(mouseX-cameraX, mouseY-cameraY)
                    playerView.focusPlayer.focusTarget = player
                  if isinstance(player, Resources.Tree):
                    zoneAction.append("Harvest")
                  elif isinstance(player, Resources.Item):
                    zoneAction.append("Pick up")
            playerView.zoneAction = zoneAction
                     
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
