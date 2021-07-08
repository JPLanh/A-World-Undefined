import pygame
import constant
import Person
import Resources
import spriteLoader
import ItemList

class Entity(pygame.sprite.Sprite):
  def __init__(self, name, entityType, mapLocation, playerView, angle, cordPosition, layer):
    pygame.sprite.Sprite.__init__(self)
    self.name = name
    self.angle = angle
    self.myMap = mapLocation
    self.playerView = playerView
    #in relative to the world
    self.pos = cordPosition
    #place on the window
    self.coordinate = self.myMap.prePosConversion(cordPosition.x+9, cordPosition.y+8, 42, 18)
    self.position = self.myMap.cordsConversion(self.pos.x, self.pos.y)
    self._layer = layer
    self.image = spriteLoader.spriteLoader(entityType).getImage(0, 0, constant.TILE_WIDTH_SIZE, constant.TILE_HEIGHT_SIZE)
    if entityType == "img/Leaf.png":    
      self.image = spriteLoader.spriteLoader(entityType).getImage(0, 0, constant.TILE_WIDTH_SIZE, constant.TILE_HEIGHT_SIZE)
      self.image.set_alpha(155)
    self.rect = self.image.get_rect(topleft=self.coordinate)

class EntityGenerator:
  def __init__(self, renderGroup, outGroup, floorGroup, mapGet, playerView):
    self.renderGroup = renderGroup
    self.outGroup = outGroup
    self.floorGroup = floorGroup
    self.mapGet = mapGet
    self.playerView = playerView

  def loadEntity(self, typeGet, name, xGet, yGet, angle):
#    cordPosition = self.mapGet.prePosConversion(xGet, yGet, 42, 18)
    cordPosition = pygame.math.Vector2(xGet, yGet)
    if typeGet == "Player":
      tempEntity = Person.Person(name, self.mapGet, self.playerView,
                                 cordPosition, angle, 250)
      self.renderGroup.add(tempEntity)
    elif typeGet == "Resource":
      if (name == "Tree"):
        print("Tree load")
        tempEntity = Resources.HarvestableNode(name, self.mapGet, self.playerView,
                                 cordPosition, angle, 25)
        self.renderGroup.add(tempEntity)
        tempEntity = Resources.NonHarvestableNode(name, self.mapGet, self.playerView,
                                 cordPosition, angle, 30)      
        self.renderGroup.add(tempEntity)
    elif typeGet == "Wall":
      tempEntity = Resources.Wall(name, self.mapGet, self.playerView,
                                 cordPosition, angle, 25)
      self.renderGroup.add(tempEntity)
    elif typeGet == "Item":
      cordPosition = pygame.math.Vector2((constant.TILE_WIDTH_SIZE*xGet,constant.TILE_HEIGHT_SIZE*yGet))
      tempEntity = Resources.Item(name, ItemList.itemList().getItem(name),  self.mapGet, self.playerView,
                                 cordPosition, angle, 25)
      self.outGroup.add(tempEntity)
    elif typeGet == "Environment":
      tempEntity = Resources.Floor(name, ItemList.environmentList().getEnvironment(name),  self.mapGet, self.playerView,
                                 cordPosition, angle, ((xGet-8)+(yGet-9)*16))
      self.floorGroup.add(tempEntity)
      
      
