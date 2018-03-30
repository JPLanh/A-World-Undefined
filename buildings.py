class Buildings:
  def __init__(self, EG):
    self.EG = EG

  def LumberYard(self, xPos, yPos, width, length):
    for x in range (0, width):
      self.EG.loadEntity("Wall", "Wall", xPos+x, yPos, 0)
#        mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+x), 42*yPos, 'left', 50))
      if x != 4 and x != 5:
        self.EG.loadEntity("Wall", "Wall",(xPos+x),(yPos+length-1), 0)
#          mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+x), 42*(yPos+length-1), 'left', 50))
    for y in range (0, length):
      self.EG.loadEntity("Wall", "Wall",(xPos), (yPos+y), 90)
      self.EG.loadEntity("Wall", "Wall", (xPos+width-1), (yPos)+y, 90)
#      mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos), 42*(yPos+y), 'up', 50))
#      mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+width-1), 42*(yPos+y), 'up', 50))
  
