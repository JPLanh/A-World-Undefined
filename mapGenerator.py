import pygame

def generateMap(surface, map_data, TEXTURES):
  for row in map_data:
    for rect, tile_type in row:
      surface.blit(TEXTURES[tile_type], rect.topleft)

def initialize(TILE_X_SIZE, TILE_Y_SIZE):

  # The small surfaces that will be blitted on the big surface below.
  GRASS = pygame.Surface((TILE_X_SIZE, TILE_Y_SIZE))
  GRASS.fill((40, 140, 20))
  pygame.draw.rect(GRASS, (10, 100, 50), (0, 0, TILE_X_SIZE, TILE_Y_SIZE), 2)
  GROUND = pygame.Surface((TILE_X_SIZE, TILE_Y_SIZE))
  GROUND.fill((90, 40, 20))
  pygame.draw.rect(GROUND, (110, 100, 50), (0, 0, TILE_X_SIZE, TILE_Y_SIZE), 2)
  WATER = pygame.Surface((TILE_X_SIZE, TILE_Y_SIZE))
  WATER.fill((40, 70, 170))
  pygame.draw.rect(WATER, (80, 80, 190), (0, 0, TILE_X_SIZE, TILE_Y_SIZE), 2)
  FLOOR = pygame.Surface((TILE_X_SIZE, TILE_Y_SIZE))
  FLOOR.fill((120, 120, 100))
  pygame.draw.rect(FLOOR, (20, 20, 20), (0, 0, TILE_X_SIZE, TILE_Y_SIZE), 2)  

  TEXTURES = {'1': GRASS, '2': GROUND, '3': WATER, '4': FLOOR}

  # The map is a list of lists which contain pg.Rects and the tile_type.
  MAP_DATA = [[(pygame.Rect(TILE_X_SIZE*x, TILE_Y_SIZE*y, TILE_X_SIZE, TILE_Y_SIZE), '2')
               for x in range(100)]
              for y in range(100)]
  MAP_DATA[4] = [(rect, '1') for rect, _ in MAP_DATA[4]]  # A grass row.
  MAP_DATA[20] = [(rect, '3') for rect, _ in MAP_DATA[20]]  # Water.
  MAP_DATA[27] = [(rect, '4') for rect, _ in MAP_DATA[27]]  # Floor.
  # Create a big surface with the size of the map.
  BACKGROUND = pygame.Surface((TILE_X_SIZE*128, TILE_Y_SIZE*128))
  generateMap(BACKGROUND, MAP_DATA, TEXTURES)  # Blit the tiles on the image.
  return BACKGROUND
