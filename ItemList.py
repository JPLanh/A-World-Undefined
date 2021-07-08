class itemList():
  def __init__(self):
    self.items = {}
    self.items["Lumber"] = Items("Lumber", 30, 5, 1)
    self.items["Log"] = Items("Log", 75, 5, 1)
    self.items["Saw"] = Items("Saw", 5, 1, 1)

  def getItem(self, name):
    return self.items[name].imgName

class Items():
  def __init__(self, name, weight, width, height):
    self.imgName = 'img/' + str(name) + '.png'
    self.weight = weight
    self.width = width
    self.height = height

class environmentList():
  def __init__(self):
    self.environments = {}
    self.environments["Grass"] = "img/Environment/Grass.png"
    self.environments["Dirt"] = "img/Environment/Dirt.png"

  def getEnvironment(self, name):
    return self.environments[name]
