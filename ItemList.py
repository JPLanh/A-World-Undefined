import Resources

class itemList():
  def __init__(self, entityGroup):
    self.entityGroup = entityGroup
    self.items = {}
    self.items["Lumber"] = Items("Lumber", 30, 5, 1)
    self.items["Log"] = Items("Log", 75, 5, 1)
    self.items["Saw"] = Items("Saw", 5, 1, 1)

  def createItem(self, itemName, getMap, playerView, getX, getY, direction, layer):
    if self.items[itemName]:
      return Resources.Item(itemName, self.items[itemName].imgName,
                            getMap, playerView, (getX, getY), self.items[itemName].weight,
                            self.items[itemName].width, self.items[itemName].height,
                            direction, layer, self.entityGroup)

  def createWall(self, itemName, getMap, playerView, getX, getY, direction, layer):
    if self.items[itemName]:
      return Resources.Wall(itemName, self.items[itemName].imgName,
                            getMap, playerView, (getX, getY), self.items[itemName].weight,
                            self.items[itemName].width, self.items[itemName].height,
                            direction, layer, self.entityGroup)
    
class Items():
  def __init__(self, name, weight, width, height):
    self.imgName = 'img/' + str(name) + '.png'
    self.weight = weight
    self.width = width
    self.height = height
