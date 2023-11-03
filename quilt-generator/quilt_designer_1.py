'''
This sketch:

TODO:
- Add ability to load patterns
- fill block with different colors
- Different mirror types
- Edit block
- Weighted random for piece selection
- CLEAN UP code

'''
import pygame
from colors import *
import random
import time
import json

pygame.init()  
DEBUG = True

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

# screen size
XRES = 800 
YRES = 800 

# block constants
COLUMNS = 8
ROWS = COLUMNS
PIECE_WIDTH = 48 # TODO make scale
PIECE_COUNT = ROWS * COLUMNS
GRID_OFFSET_X = (XRES - (PIECE_WIDTH * COLUMNS))/2
GRID_OFFSET_Y = (YRES - (PIECE_WIDTH * ROWS))/2
BLOCK_WIDTH = COLUMNS * PIECE_WIDTH

FONT = pygame.font.SysFont("retrogaming", 16) 
FONT_BIG = pygame.font.SysFont("retrogaming", 24) 
FONT_HUGE = pygame.font.SysFont("retrogaming", 48) 

DARK_COLORS = (BLUE, GREEN, BLACK, GRAY, PURPLE, NAVY, RED)
LIGHT_COLORS = (WHITE, CREAM, RED, RED_ORANGE, TEAL, LIME, BEIGE)

screen = pygame.display.set_mode((XRES,YRES))    

###############################################################################
###############################################################################     

class Piece():
    def __init__(self, type, pos, rotation = 0, light_color = CREAM, dark_color = NAVY):
        self.type = type          # 0,1,2 for full_dark, full_light or diag
        self.pos = pos            # (r, c)
        self.rotation = rotation         # default rotation
        self.light_color = light_color   # default light color
        self.dark_color = dark_color     # default dark color
        self.rect = self.create_rect(pos)
        self.small_rect = self.create_small_rect(pos)
        
        # ROTATION:
        # 0:  light / dark
        # 1:  dark \ light
        # 2:  dark / light
        # 3:  light \ dark      
        
    def create_rect(self, pos):
        
        # get the rect position based on the space the tile is in       
        x = (pos[1] * PIECE_WIDTH) + GRID_OFFSET_X
        y = (pos[0] * PIECE_WIDTH) + GRID_OFFSET_Y
        
        return pygame.Rect(x, y, PIECE_WIDTH, PIECE_WIDTH)
    
    def create_small_rect(self, pos):
        # 1/4 of regular size
        x = (pos[1] * (PIECE_WIDTH / 4)) + GRID_OFFSET_X
        y = (pos[0] * (PIECE_WIDTH / 4)) + GRID_OFFSET_Y
        
        return pygame.Rect(x, y, PIECE_WIDTH / 4, PIECE_WIDTH / 4) 
    
    def get_dict(self):
        obj_dict = {'type': self.type, 'pos': self.pos, 'rotation': self.rotation, 'light_color': self.light_color, 'dark_color': self.dark_color}
    
        return obj_dict     
    
class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
            obj_dict = {'type': obj.type, 'pos': obj.pos, 'rotation': obj.rotation, 'light_color': obj.light_color, 'dark_color': obj.dark_color}
    
            return obj_dict        

        
class Color():
    def __init__(self, color, color_type, pos):
        self.pos = pos  # (xres, yres)
        self.color = color
        self.color_type = color_type # 0 for dark, 1 for light
        self.rect = pygame.Rect(self.pos[0], self.pos[1], PIECE_WIDTH, PIECE_WIDTH)

###############################################################################
###############################################################################

def init_block():
    # create an empty 2D list to store pieces:
    block = []
    for r in range(ROWS):
        block.append([])
        for c in range(COLUMNS):
            block[r].append(None)
            
    return block
    
def draw_placeholder_grid():
    # starting at the grid offset, draw rects represent the open spots for the block
    for r in range(ROWS):
        for c in range(COLUMNS):
            x = (c * PIECE_WIDTH) + GRID_OFFSET_X
            y = (r * PIECE_WIDTH) + GRID_OFFSET_Y
            pygame.draw.rect(screen, DARK_GRAY, (x, y, PIECE_WIDTH, PIECE_WIDTH), 1)

def create_color_options(dark_colors, light_colors):
    # create color objects based on the colors provided
    
    colors = []
    
    # for color in dark_colors:
    for i, color in enumerate(dark_colors):
        x = (i * PIECE_WIDTH) + GRID_OFFSET_X
        y = GRID_OFFSET_Y + BLOCK_WIDTH + (YRES - (GRID_OFFSET_Y + BLOCK_WIDTH))/2  # halfway between bottom of block and bottom
        
        # create a color object with that color at a unique position
        new_color = Color(color, 0, (x,y))
        colors.append(new_color)
        
    # for color in light_colors:
    for i, color in enumerate(light_colors):
        x = (i * PIECE_WIDTH) + GRID_OFFSET_X
        y = PIECE_WIDTH + GRID_OFFSET_Y + BLOCK_WIDTH + (YRES - (GRID_OFFSET_Y + BLOCK_WIDTH))/2  # One row below dark colors
        
        # create a color object with that color at a unique position
        new_color = Color(color, 1, (x,y))
        colors.append(new_color)
        
    return colors

def draw_color_options(colors):
    
    for color in colors:
        pygame.draw.rect(screen, color.color, color.rect)
        
def create_piece_options():
    # create default piece objects 
    num_piece_options = 3
    piece_options = []
    
    for i in range(num_piece_options):

        x = i  # fake row i (as we're specifying location based on the block now
        y = 10 # fake col 10
        
        piece_type = i # 0, 1, 2 for dark, light, diagnoal
        
        # create a piece object with that color at a unique position
        new_piece = Piece(piece_type, (x,y))
        print(new_piece.rect.left)
        piece_options.append(new_piece)
        
    return piece_options

def rotate_piece_options(piece_options):
    
    for piece in piece_options:
        if piece.rotation < 3:
            piece.rotation += 1
        else:
            piece.rotation = 0
            
def update_colors(color_obj, piece_options):
    for piece in piece_options:
        if color_obj.color_type == 0:
            piece.dark_color = color_obj.color
        if color_obj.color_type == 1:
            piece.light_color = color_obj.color

def random_fill(block):
    # fill the top left quadrant of the block with random pieces
    for r in range(int(ROWS/2)):
        for c in range(int(COLUMNS/2)):
                      
            piece_type = random.choice((0,1,2))
            
            block[r][c] = Piece(piece_type, (r,c))  
            
            # TODO Make Optional
            # randomly rotate block if it's a diagonal
            if block[r][c].type == 2:
                rotation = random.choice((0,1,2,3))
                block[r][c].rotation = rotation
            
    
    return block

def mirror_pieces(block, mirror_type):
    
    # Get the pieces from the top left quarter (ROWS/2, COLS/2)
    for r in range(int(ROWS/2)):
        for c in range(int(COLUMNS/2)):
        
            # fill top right quadrant:
            # add copies of top left to top right
            new_col = COLUMNS - 1 - c
            new_row = r
            type = block[r][c].type
            light_col = block[r][c].light_color
            dark_col = block[r][c].dark_color
            
            if mirror_type == 1:
                # positional mirror, no rotation mirroring
                rotation = block[r][c].rotation
            elif mirror_type == 2:
                # positional mirroring and rotation mirroring
                if block[r][c].rotation == 0 or block[r][c].rotation == 2:
                    rotation = block[r][c].rotation + 1
                else:
                    rotation = block[r][c].rotation - 1
                       
            block[new_row][new_col] = Piece(type, (new_row, new_col), rotation, light_col, dark_col)
            #print(f"Right quad row {r}, col {COLUMNS - 1 - c} = {block[r][c].type} at position ({x},{y})")
            
            # fill bottom left quadrant:
            new_col = c
            new_row = ROWS - 1 - r
            type = block[r][c].type
            light_col = block[r][c].light_color
            dark_col = block[r][c].dark_color
            
            if mirror_type == 1:
                # positional mirror, no rotation mirroring
                rotation = block[r][c].rotation
            elif mirror_type == 2:
                # positional mirroring and rotation mirroring
                if block[r][c].rotation == 0:
                    rotation = 3
                elif block[r][c].rotation == 3:
                    rotation = 0
                elif block[r][c].rotation == 1:
                    rotation = 2
                else:
                    rotation = 1
                       
            block[new_row][new_col] = Piece(type, (new_row, new_col), rotation, light_col, dark_col)
            
            
            # fill bottom right quadrant:
            new_col = COLUMNS - 1 - c
            new_row = ROWS - 1 - r
            type = block[r][c].type
            light_col = block[r][c].light_color
            dark_col = block[r][c].dark_color
            
            if mirror_type == 1:
                # positional mirror, no rotation mirroring
                rotation = block[r][c].rotation
            elif mirror_type == 2:
                # positional mirroring and rotation mirroring
                if block[r][c].rotation == 0 or block[r][c].rotation == 1:
                    rotation = block[r][c].rotation + 2
                else:
                    rotation = block[r][c].rotation - 2
                       
            block[new_row][new_col] = Piece(type, (new_row, new_col), rotation, light_col, dark_col)
            
            # [0],[0] should be mirrored to:
            # - [0],[7]: right 
            # - [7],[0]: dowm
            # - [7],[7]: downright
            
            # [0],[3] should be mirrored to:
            # - [0],[4]: right
            # - [7],[3]: down
            # - [7],[4]: downright
            
            # [3],[0] should be mirrored to:
            # - [3],[7]:  right
            # - [4],[0]: down
            # - [4],[7]: downright
            
            # [3],[3] should be mirrored to:
            # - [3],[4]:  right
            # - [4],[3]: down
            # - [4],[4]: downright
            
            
            # ROTATION:
            # 0:  light / dark --> Right: 0->1, Down: 0->3, Downright: 0->2
            # 1:  dark \ light --> Right: 1->0, down: 1->2, downright: 1->3
            # 2:  dark / light --> right: 2->3, down: 2->1, Downright: 2->0
            # 3:  light \ dark --> right: 3->2, Down: 3->0, downright: 3->1
    
    return block
    
def draw_piece(piece, pos_offset, size):
    
    if size == 'regular':
        left = piece.rect.left
        right = piece.rect.right 
        top = piece.rect.top 
        bottom = piece.rect.bottom 
        w = piece.rect.width
        h = piece.rect.height
    
    if size == 'small':
        left = piece.small_rect.left + pos_offset[0]
        right = piece.small_rect.right + pos_offset[0]
        top = piece.small_rect.top + pos_offset[1]
        bottom = piece.small_rect.bottom + pos_offset[1]
        w = piece.small_rect.width
        h = piece.small_rect.height
        
    # if full dark
    if piece.type == 0:
        pygame.draw.rect(screen, piece.dark_color, (left, top, w, h))
    
    # if full light
    elif piece.type == 1:
        pygame.draw.rect(screen, piece.light_color, (left, top, w, h))
    
    # if diagonal 
    elif piece.type == 2:
        if piece.rotation == 0: 
            # light / dark
            pygame.draw.polygon(screen, piece.light_color, ((left, top), (right, top), (left, bottom)))
            pygame.draw.polygon(screen, piece.dark_color, ((left, bottom), (right, top), (right, bottom)))
        elif piece.rotation == 1: 
            # dark \ light
            pygame.draw.polygon(screen, piece.light_color, ((left, top), (right, top), (right, bottom)))
            pygame.draw.polygon(screen, piece.dark_color, ((left, top), (right, bottom), (left, bottom)))
        elif piece.rotation == 2: 
            # dark / light
            pygame.draw.polygon(screen, piece.dark_color, ((left, top), (right, top), (left, bottom)))
            pygame.draw.polygon(screen, piece.light_color, ((left, bottom), (right, top), (right, bottom)))
        elif piece.rotation == 3: 
            # light \ dark
            pygame.draw.polygon(screen, piece.dark_color, ((left, top), (right, top), (right, bottom)))
            pygame.draw.polygon(screen, piece.light_color, ((left, top), (right, bottom), (left, bottom)))

def draw_piece_options(piece_options):
    for piece in piece_options:
        draw_piece(piece, (0,0), 'regular')
    
def draw_block(block, pos, piece_size):
    #print(f"{piece_size} Block being drawn, block has {len(block)} rows and {len(block[0])} columns")
    for r, row in enumerate(block):
        if row is not None: 
            for piece in block[r]:
                if piece is not None:
                    if piece_size == 'regular': 
                        draw_piece(piece, pos, 'regular')
                    if piece_size == 'small': 
                        draw_piece(piece, pos, 'small')
  
def draw_quilt(block):
    
    q_rows = 5
    q_cols = 4
    
    sm_block_width = BLOCK_WIDTH / 4
    
    for r in range(q_rows):
        for c in range(q_cols):
            x = c * sm_block_width
            y = r * sm_block_width
            draw_block(block, (x,y), 'small')
            
            
    
    # draw a quilt, 4 blocks wide, 6 blocks tall
    pass
              
def save_to_json(block, mirror_type):
    # save block to JSON
    block_dict = {}
    piece_dicts = []

    for r,row in enumerate(block):
        for col in block[r]:
            piece_dict = col.get_dict()
            piece_dicts.append(piece_dict)
    
    block_dict['mirror'] = mirror_type
    block_dict['pieces'] = piece_dicts
    timestr = time.strftime("%Y-%m-%d-%H%M%S")
    
    with open(f"quilt_block_{timestr}.json", "w") as write_file:
        json.dump(block_dict, write_file, indent=4) 
    
########################################
# GAME STARTUP
########################################
mode = 'design'
mirror_type = 2
selected_piece_option = None

# the actual block that will hold piece objects
block = init_block()

# create dark & light color options
colors = create_color_options(DARK_COLORS, LIGHT_COLORS)

# create peice options
piece_options =  create_piece_options() 


########################################
# Main Game Loop
########################################
while True:
    screen.fill(BLACK)     # clear screen 
    
    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_s:
                # save block to JSON
                save_to_json(block, mirror_type)            
            if event.key == pygame.K_RETURN:
                # random generate top right quarter of block
                block = random_fill(block)
                block = mirror_pieces(block, mirror_type)
            if event.key == pygame.K_r:
                # rotate pieces to select from
                rotate_piece_options(piece_options)
            if event.key == pygame.K_q:
                if mode == 'design':
                    mode = 'quilt_preview'
                else:
                    mode = 'design'
        
        # if LEFT MOUSE button clicked, check if it collides with anything
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            pos = pygame.mouse.get_pos()
            
            # check if cursor is on a color cell. if so update piece option colors.
            for color in colors:
                if color.rect.collidepoint(pos):
                    update_colors(color, piece_options)
                    
            # check if cursor is on a piece option cell. if so update the selected piece option.
            for piece in piece_options:
                if piece.rect.collidepoint(pos):
                    selected_piece_option = piece
                    
            # check if cursor is on a piece block piece. if so update the selected piece with the piece option.
            for r, row in enumerate(block):
                for piece in block[r]:
                    if piece.rect.collidepoint(pos):
                        piece.type = selected_piece_option.type
                        piece.rotation = selected_piece_option.rotation
                        piece.dark_color = selected_piece_option.dark_color
                        piece.light_color = selected_piece_option.light_color
                               
            
    if mode == 'design':
        # draw placeholder grid to fill   
        draw_placeholder_grid()

        # draw dark & light color options
        draw_color_options(colors)
        
        # draw pieces
        draw_piece_options(piece_options)
        if selected_piece_option:
            pygame.draw.rect(screen, RED, selected_piece_option.rect, 2)
            
        draw_block(block, (GRID_OFFSET_X, GRID_OFFSET_Y), 'regular')
        
    if mode == 'quilt_preview':
        # draw_quilt
        draw_quilt(block)
    
  
    
        
            
            
                
    pygame.display.update()
    fpsClock.tick(FPS)