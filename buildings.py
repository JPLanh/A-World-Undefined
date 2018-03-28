class Lumberyard:
  def __init__(self, itemGenerator, mapGet, playerView, xPos, yPos, width, length): 
    for x in range (0, width):
        mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+x), 42*yPos, 'left', 50))
        if x != 4 and x != 5:
          mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+x), 42*(yPos+length-1), 'left', 50))
    for y in range (0, length):
      mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos), 42*(yPos+y), 'up', 50))
      mapGet.entityList.append(itemGenerator.createWall("Lumber", mapGet, playerView, 42*(xPos+width-1), 42*(yPos+y), 'up', 50))
  
