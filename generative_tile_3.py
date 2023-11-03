'''
What this sketch does:
- Creates a square 'board' of n spaces
- Fills the board with N-1 tiles in random positions
  - Colors the tiles randomly
- Runs a script that iterates through the tiles and:
  - Checks if there are open spaces next (up,down,left,right) to the tile
  - If so, randomly picks one of the directions that is open
  - Moves the tile (either 1 space or until a collision occurs)
'''

import pygame
import colors
from time import sleep
import random
import math

XRES = 800
YRES = 800

DEBUG = False

screen = pygame.display.set_mode((XRES,YRES))
screen.fill(colors.BLACK)
clock = pygame.time.Clock()

ROW_COUNT = 32
COL_COUNT = ROW_COUNT
TOTAL_SPACES = ROW_COUNT * COL_COUNT
TOTAL_TILES = int(TOTAL_SPACES * .5)
SPACE_SIZE = int(XRES / COL_COUNT)
TILE_SIZE = [XRES / COL_COUNT, YRES / ROW_COUNT]
DIRECTIONS = [[0,-1],[0,1],[-1,0],[1,0]]

move_count = int(TOTAL_TILES / 5)    # Tiles to move
move_amount = SPACE_SIZE / 5  # CAREFUL, must be a multiple of SPACE_SIZE

SHAPES = ['vert','horiz','diag_down','diag_up'] # 'cross','arc_open_top','arc_open_bottom'

TRANS_RED = (255,0,0,200)
TRANS_GREEN = (0,255,0,200)
TRANS_BLUE = (0,0,255,200)
COLORS = [TRANS_RED, colors.WHITE]
PI = math.pi



# List to store whether or not a space is occupied by a tile
space_occupied = []
for space in range(TOTAL_SPACES):
    space_occupied.append(0) # set all spaces as open

# Initialize an empty board list. Will be filled with tile objects
board = []
for row in range(ROW_COUNT):
    board.append([])
    for col in range(COL_COUNT):
        board[row].append(0)
        
def print_board():
    # board[row num][column num]
    print('')
    for row in range(ROW_COUNT):
        print(board[row])
    print('')

class Tile:
    
    def __init__(self, id, board):
        self.id = id
        self.color = random.choice(COLORS)  
        self.shape = random.choice(SHAPES)
        self.pos = self.select_random_open_space(board)  
        self.pixel_pos = self.get_pixel_pos(self.pos)  # the actual location of the tile (even in transit)
        self.dir = [0,0]
        self.move_attempt_count = 1 # each tile will try twice to make a move each round
        self.destination_reached = True 
        self.tile_rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], TILE_SIZE[0], TILE_SIZE[1])
    
    def select_random_open_space(self, board):
        # Find a space that is open. If occupied, look again.
        pos = [0,0]
        space_found = False
        
        while space_found == False: 
            x_to_check = random.randint(0,ROW_COUNT - 1)
            y_to_check = random.randint(0,COL_COUNT - 1)
            
            if board[y_to_check][x_to_check] == 0:
                pos = [x_to_check, y_to_check]
                space_found = True
               
        return pos    
    
    
    def get_pixel_pos(self, pos):
        # get the rect position based on the space the tile is in
        pixel_pos = [pos[0] * SPACE_SIZE, pos[1] * SPACE_SIZE]
       
        return pixel_pos
    
    def neighbor_open_check(self, dir, board): 
        # at this point self.pos is the tile's CURRENT position  
        # For one tile at time, it's ok to check the current positions of the OTHER tiles
        # For all tiles at once, we need to check the destination position of OTHER tiles, which should be updated each time a destination is selected   
        # First check if in bounds
        max = [COL_COUNT - 1, ROW_COUNT - 1]
        
        if 0 <= self.pos[0] + dir[0] <= max[0] and 0 <= self.pos[1] + dir[1] <= max[1]: 
            
            # if not out of bounds, see if the neighbor space is full
            space_contents = board[self.pos[1] + dir[1]][self.pos[0] + dir[0]]
            
            if DEBUG: print("Checking neighbor in direction:",dir, "Looks like it contains:",space_contents)
            
            if space_contents == 0:
                return dir  # say that this direction is open
            else:
                return [0, 0] # say that the direction isn't available
        else:
            if DEBUG: print("Checking neighbor in direction:", dir, "Looks like it's out of bounds")
            return [0, 0] # say that the direction is out of bounds
            
    def update_destination(self, dir, board):
        
        self.destination_reached = False
        destination_determined = False
        
        # mark old board position as open:
        board[self.pos[1]][self.pos[0]] = 0
        
        if DEBUG: print("\nUpdating dest for tile", self.id, "Orig position:", self.pos, "Moving direction:", dir)
        
        # TODO: retry this using a while loop instead??
        for i in range(ROW_COUNT):
            # Move tile position in the direction
            x = self.pos[0] + dir[0]
            y = self.pos[1] + dir[1]
            self.pos = [x,y]  
            
            if DEBUG: print("New position for tile", self.id, self.pos)
            
            # Check if the new position has open spaces in the same direction (returns the direction if open)
            dir = self.neighbor_open_check(dir, board)
            if DEBUG: ("In update_destination function, neighbor_open_check returned:", dir)
            
            # if no direction returned from neighbor check (dir is [0,0]) exit this loop
            if dir[0] == 0 and dir[1] == 0: 
                break
                                      
        
        if DEBUG: print("New destination:", self.pos, "which has pixel xy postion:",self.get_pixel_pos(self.pos))
        
        # mark new board position (desination) as closed
        board[self.pos[1]][self.pos[0]] = self.id
        
        return board
    
    def move_to_destination(self, dir):
        destination = self.get_pixel_pos(self.pos)
        if DEBUG: print("Moving tile", self.id,"in direction:", dir, "towards Destination pixel pos:", destination, "current pixel pos:",self.pixel_pos)
        # if the tile's current position isn't eq to the pixel position of the destination
        if self.pixel_pos != destination:
            # move the tile X pixels in the direction of the desitnation
            self.pixel_pos[0] += (dir[0] * move_amount)
            self.pixel_pos[1] += (dir[1] * move_amount)
            self.tile_rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], TILE_SIZE[0], TILE_SIZE[1])
        else:
            if DEBUG: print("Destination Reached")
            self.destination_reached = True
            
def update_tile_destinations(tiles, start_tile, move_count, board):
    
    shifted_tiles = (tiles[start_tile:]) + tiles[:start_tile]  # slice list and rebuild so that you can wrap around
    tiles_to_move = [] # list to store which tiles we need to move based on which ones have open positions next to them
    
    # iterate through the "tile to move" and N more tiles
    for tile in shifted_tiles[:move_count]:
        
        available_moves = []
        #tile.dir = [0,0]  # default direction - no movement
        
        if DEBUG: print("\nUpdating the destination for tile #:", tile.id, "Current position:", tile.pos)
        if DEBUG: print_board()
        
        # Select first dimension to move in randomly:
        if tile.move_attempt_count == 1: 
            
            if DEBUG: print("Move attempt 1. Pick a random direction")
            
            for dir in DIRECTIONS:  # up, down, left, right
                direction = tile.neighbor_open_check(dir, board)
                             
                # if a real direction returns, add it to the open direction list
                if direction[0] == 0 and direction[1] == 0: 
                    pass  # no available direction found
                else:
                    available_moves.append(direction)   
            
        
        # Attempt to define destination for the second dimension move:
        if tile.move_attempt_count == 2: 
            if DEBUG: print("Move attempt 2. Pick a direction oposite axis to the first direction:", tile.dir)

            if tile.dir[0] == 0:    # was up/down
                for dir in [[-1,0],[1,0]]:  # move left/right
                    direction = tile.neighbor_open_check(dir, board)
                    if direction[0] != 0 or direction[1] != 0: 
                        available_moves.append(direction)   
            elif tile.dir[1] == 0:  # was left/right
                for dir in [[0,-1],[0,1]]:  # up, down
                    direction = tile.neighbor_open_check(dir, board)
                    if direction[0] != 0 or direction[1] != 0: 
                        available_moves.append(direction)   
            
        # if there are one or more available move directions, pick a direction 
        if available_moves: 
            tile.dir = random.choice(available_moves) # select one of the open directions to move the tile in
            if DEBUG: print("New tile direction is:", tile.dir)
            board = tile.update_destination(tile.dir, board)
            tiles_to_move.append(tile)
            
    return tiles_to_move


def move_tiles(tiles_to_move):           
    for tile in tiles_to_move:
        # move the tile in a step in the correct direction
        tile.move_to_destination(tile.dir)
        
        # once the destination is reached, you can kick the tile
        if tile.destination_reached == True:
            tiles_to_move.remove(tile)
                          
    return tiles_to_move

def update_move_attempts(tiles, start_tile, move_count):
    shifted_tiles = (tiles[start_tile:]) + tiles[:start_tile]  # slice list and rebuild so that you can wrap around
    for tile in shifted_tiles[:move_count]:
        if tile.move_attempt_count == 1:
            tile.move_attempt_count = 2
            if DEBUG: print("Tile", tile.id, "move attemp changed from 1 to 2.")
        elif tile.move_attempt_count == 2:
            tile.move_attempt_count = 1
            if DEBUG: print("Tile", tile.id, "move attemp changed from 2 to 1.")
        
    
    
def draw_tiles(tile):
    if tile.shape == 'vert':
        pygame.draw.line(screen, tile.color, [tile.tile_rect.left, tile.tile_rect.top],[tile.tile_rect.left, tile.tile_rect.bottom], 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.right, tile.tile_rect.top],[tile.tile_rect.right, tile.tile_rect.bottom], 2)
    elif tile.shape == 'horiz':
        pygame.draw.line(screen, tile.color, [tile.tile_rect.left, tile.tile_rect.top],[tile.tile_rect.right, tile.tile_rect.top], 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.left, tile.tile_rect.bottom],[tile.tile_rect.right, tile.tile_rect.bottom], 2)
    elif tile.shape == 'diag_down':
        pygame.draw.line(screen, tile.color, tile.tile_rect.topleft, tile.tile_rect.bottomright, 2)
    elif tile.shape == 'diag_up':
        pygame.draw.line(screen, tile.color, tile.tile_rect.bottomleft, tile.tile_rect.topright, 2)
    elif tile.shape == 'cross':
        pygame.draw.line(screen, tile.color, tile.tile_rect.topleft, tile.tile_rect.bottomright, 2)
        pygame.draw.line(screen, tile.color, tile.tile_rect.topright, tile.tile_rect.bottomleft, 2)
    elif tile.shape == 'arc_open_top':
        # need to add 1 pixel to width of rect for ard to hit right
        pygame.draw.arc(screen, tile.color, tile.tile_rect, PI, 2*PI, 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.left, tile.tile_rect.centery],[tile.tile_rect.left, tile.tile_rect.top], 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.right - 2, tile.tile_rect.centery],[tile.tile_rect.right - 2, tile.tile_rect.top], 2)
    elif tile.shape == 'arc_open_bottom':
        pygame.draw.arc(screen, tile.color, tile.tile_rect, 0, PI, 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.left, tile.tile_rect.centery],[tile.tile_rect.left, tile.tile_rect.bottom], 2)
        pygame.draw.line(screen, tile.color, [tile.tile_rect.right - 2, tile.tile_rect.centery],[tile.tile_rect.right - 2, tile.tile_rect.bottom], 2)            

###  STARTUP SEQUENCE ####
# Create tile objects:
tiles = []
for tile in range(TOTAL_TILES):
    new_tile = Tile(tile+1, board)
    tiles.append(new_tile)
    
    # Fill the board list:
    if DEBUG: print("Original tile position for tile:",new_tile.id, new_tile.pos)
    board[new_tile.pos[1]][new_tile.pos[0]] = new_tile.id  # board[row num ie height/y][column num ie width/x]

if DEBUG: print_board()

loop_count = 0
start_tile = 1
dimension = 1   # toggle between 1 and 2
set_new_destinations = True
pause = False

###  RUN LOOP ###
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
            if event.key == pygame.K_p:
                pause = not pause
            
    # Update destinatations for the tiles
    # Step 1: Pick a random open direction.
    # Step 2: Select a positiom in that direction until the direction is no longer open
    # Step 3: Move to that position
    # Step 4: Pick a random *oposite* open direction
    # Step 4: Move in that direction until the direction is no longer open
    # Step 5: Once all tiles in the group have done the above, move to the next group
    if set_new_destinations: 
        tiles_to_move = update_tile_destinations(tiles, start_tile, move_count, board)
        set_new_destinations = False
    
    if tiles_to_move:
        # if there are one or more tiles to move
        tiles_to_move = move_tiles(tiles_to_move)
    else:
        # If moving in dimension 1: go back to set_new_destinations to pick 2D dest for same group of tiles
        if dimension == 1:
            update_move_attempts(tiles, start_tile, move_count)
            dimension = 2
            set_new_destinations = True 
        elif dimension == 2: 
            # If moving in dimension 2: once all destinations reached, then update the start tile for the next group of tiles to move
            start_tile = (start_tile + move_count) % TOTAL_TILES
            dimension = 1
            set_new_destinations = True 
        
    # draw the tiles
    for tile in tiles:
        # draw colorful rectangles
        #draw_rect_alpha(screen, tile.color, tile.tile_rect)
       
        # or draw line shapes
        draw_tiles(tile)

            
    pygame.display.update()
    clock.tick(30)
