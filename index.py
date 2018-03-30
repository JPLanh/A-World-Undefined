
import pygame
import math
import time

import constant
import node
import mapGenerator
import Person
import Camera
import Resources
import ItemList
import Entity
import menu
import buildings

pygame.init()

mapOne = node.Graph(constant.MAX_X_TILES,constant.MAX_Y_TILES)

gameDisplay = pygame.display.set_mode((constant.TILE_WIDTH*constant.TILE_WIDTH_SIZE,constant.TILE_HEIGHT*constant.TILE_HEIGHT_SIZE))
pygame.display.set_caption('A simulation')
playerView = Camera.Camera(gameDisplay, mapOne)
clock = pygame.time.Clock()

entityGroup = pygame.sprite.LayeredUpdates()
outGroup = pygame.sprite.LayeredUpdates()
floorGroup = pygame.sprite.LayeredUpdates()

entitymover = None

EG = Entity.EntityGenerator(entityGroup, outGroup, floorGroup, mapOne, playerView)
buildingMacro = buildings.Buildings(EG)

for j in range(0, 14):
  for i in range(0, 16):      
    EG.loadEntity("Environment", "Grass", i, j, 0)
EG.loadEntity("Player", "Jimmy", 0, 0, 270)
##EG.loadEntity("Resource", "Tree", 12, 12, 270)
##EG.loadEntity("Resource", "Tree", 12, 13, 270)
##EG.loadEntity("Resource", "Tree", 13, 13, 270)
##EG.loadEntity("Resource", "Tree", 12, 11, 270)
##EG.loadEntity("Resource", "Tree", 13, 12, 270)
##EG.loadEntity("Item", "Log", 8, 7, 90)
##buildingMacro.LumberYard(5, 0, 10, 7)
#mapOne.entityList.append(itemGenerator.createItem("Log", mapOne, playerView, 42*8, 42*7, 'left', 2))
#buildings.Lumberyard(itemGenerator, mapOne, playerView, 5, 0, 10, 7)
#mapOne.entityList.append(itemGenerator.createItem("Saw", mapOne, playerView, 42*6, 42*5, 'left', 7))


def updates():
#  gameDisplay.blit(BACKGROUND, (0, 0)+playerView.cameraPos)
  gameDisplay.fill((0, 0, 0))
  floorGroup.update()
  entityGroup.update()
  outGroup.update()
  floorGroup.draw(gameDisplay)
  entityGroup.draw(gameDisplay)


##  entitymover = []
##  entityremover = []
##  for i in entityGroup:
##    if i.pos.x < -playerView.cameraPos.x+100 or i.pos.x > -playerView.cameraPos.x + 700 or i.pos.y < -playerView.cameraPos.y+300 or i.pos.y > -playerView.cameraPos.y + 500: 
##        entitymover.append(i)
##
##  for i in outGroup:
##    if i.pos.x >= -playerView.cameraPos.x+100 and i.pos.x <= -playerView.cameraPos.x +700:
##      if i.pos.y >= -playerView.cameraPos.y+300 and i.pos.y <= -playerView.cameraPos.y + 500:
##        entityremover.append(i)
##        
##  if entitymover != None:
##    for x in entitymover:  
##      outGroup.add(x)
##      entityGroup.remove(x)
##  if entityremover != None:
##    for x in entityremover:    
##      entityGroup.add(x)
##      outGroup.remove(x)      
  playerView.update()
  pygame.display.flip()

  #fps configuration
  clock.tick(45)

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

      elif event.type == pygame.KEYUP:
        if event.key == pygame.K_a:
          playerView.cameraPos.x += 42
          playerView.cameraOffset.x += 1
        if event.key == pygame.K_d:
          playerView.cameraPos.x -= 42
          playerView.cameraOffset.x -= 1
        if event.key == pygame.K_w:
          playerView.cameraPos.y += 18
          playerView.cameraPos.x -= 18
          playerView.cameraOffset.y += 1
        if event.key == pygame.K_s:
          playerView.cameraPos.y -= 18
          playerView.cameraPos.x += 18
          playerView.cameraOffset.y -= 1
#        if event.key == pygame.K_a:
#            playerView.vel.x = +48
#        if event.key == pygame.K_d:
#            playerView.vel.x = -48
#        if event.key == pygame.K_s:
#            playerView.vel.y = -18
#        if event.key == pygame.K_w:
#            playerView.vel.y = +18

#      elif event.type == pygame.KEYUP:
#        if event.key in (pygame.K_a, pygame.K_d):
#          playerView.vel.x = 0
#        elif event.key in (pygame.K_w, pygame.K_s):
#          playerView.vel.y = 0

      elif event.type == pygame.MOUSEBUTTONDOWN:
        mouseX, mouseY = pygame.mouse.get_pos()
        cameraX, cameraY = playerView.cameraPos
        xMouseTile, yMouseTile = mapOne.posConversion(mouseX, mouseY, 42, 18)
        
        if event.button == 1:
          if xMouseTile >= 0 and yMouseTile >= 0:
            getTile = playerView.getPosition(xMouseTile, yMouseTile)
            for selected in entityGroup:
              print("%d, %d" %(selected.position, getTile))
              if selected.position == getTile:
                if isinstance(selected, Person.Person):
                  playerView.focusPlayer = selected

          elif event.button == 3:
            if playerView.focusPlayer:
              playerView.focusPlayer.stopAction()
              movable = True
              playerView.zonePosition = None
              zoneAction = []
              zoneAction.append("Move")
              for player in entityGroup:
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
                    if isinstance(player, Resources.HarvestableNode):
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
