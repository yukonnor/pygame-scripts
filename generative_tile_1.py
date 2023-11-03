'''
What this sketch does:
- Creates a square 'board' of n spaces
- Fills the board with N-1 tiles in random positions
  - Colors the tiles randomly
- Runs a loop that creates the random tiles to make an animation
'''

import pygame
import colors
from time import sleep
import random

XRES = 800
YRES = 800

screen = pygame.display.set_mode((XRES,YRES))
screen.fill(colors.BLACK)

ROW_COUNT = 4
COL_COUNT = 4
TOTAL_SPACES = ROW_COUNT * COL_COUNT
TOTAL_TILES = int(TOTAL_SPACES * .6)
SPACE_SIZE = [XRES / COL_COUNT, YRES / ROW_COUNT]
TILE_SIZE = [XRES / COL_COUNT, YRES / ROW_COUNT]

# List to store whether or not a space is occupied by a tile
space_occupied = []
for space in range(TOTAL_SPACES):
    space_occupied.append(0) # set all spaces as open

class Tile:
    
    def __init__(self):
        self.color = random.choice([colors.RED, colors.GREEN, colors.BLUE])
        self.space = self.select_random_open_space()
        self.pos = self.get_pos_from_space(self.space)
        tile_rect = pygame.Rect(self.pos[0], self.pos[1], TILE_SIZE[0], TILE_SIZE[1])
        pygame.draw.rect(screen, self.color, tile_rect)
    
    def select_random_open_space(self):
        # Find a space that is open. If occupied, look again.
        space_found = False 
        
        while space_found == False: 
            space_to_check = random.randint(0,TOTAL_SPACES-1)
            
            if space_occupied[space_to_check] == 0:
                space_found = True
        
        return space_to_check    
    
    def get_pos_from_space(self, space):
        # get the rect position based on the space the tile is in
        pos = [0,0]
        
        for row in range(ROW_COUNT):
            for col in range(COL_COUNT):
                if space == col + (row * 4):
                    pos[0] = col * SPACE_SIZE[0]
                    pos[1] = row * SPACE_SIZE[1]
        
        return pos

    

while True:

    screen.fill(colors.BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                reset_face = True
                
    for tile in range(TOTAL_TILES):
        new_tile = Tile()
    

    sleep(.5)
    pygame.display.update()
