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

# TBD
PIECE_WIDTH = XRES/(2 * 8) # TODO make scale (in order to do this you need to redo how you draw the piece options)
OPTIONS_PIECE_WIDTH = 50
GRID_OFFSET_X = (XRES - (PIECE_WIDTH * 8))/2
GRID_OFFSET_Y = (YRES - (PIECE_WIDTH * 8))/2

FONT = pygame.font.SysFont("retrogaming", 16) 
FONT_BIG = pygame.font.SysFont("retrogaming", 24) 
FONT_HUGE = pygame.font.SysFont("retrogaming", 48) 

DARK_COLORS = (BLUE, GREEN, BLACK, GRAY, PURPLE, NAVY, RED)
LIGHT_COLORS = (WHITE, CREAM, RED, RED_ORANGE, TEAL, LIME, BEIGE)

screen = pygame.display.set_mode((XRES,YRES))    

###############################################################################
###############################################################################     

class Piece():
    def __init__(self, type, rotation = 0, x = 0, y = 0, width = 50, light_color = CREAM, dark_color = NAVY):
        self.type = type          # 0,1,2 for full_dark, full_light or diag
        self.rotation = rotation         # default rotation
        self.x = x                # x placement (top left corner of rect)
        self.y = y                # y placement (top left corner of rect)
        self.width = width        # The default (large, detail view) width of the piece
        self.light_color = light_color   # default light color
        self.dark_color = dark_color     # default dark color

        self.rect = pygame.Rect(self.x, self.y, self.width, self.width)
        self.small_rect = pygame.Rect(self.x, self.y, self.width / 4, self.width / 4)
        
        # a piece's x,y position is based on its location in the block's 2D array. It depends on the block position.
        # a block's x,y position is based on its location in the quilt's 2D array. 

        # ROTATION:
        # 0:  light / dark
        # 1:  dark \ light
        # 2:  dark / light
        # 3:  light \ dark    

    def get_dimensions(self, size):
        """Returns the position and dimensions of the piece based on size."""
        rect = self.rect if size == 'regular' else self.small_rect
        return rect.left, rect.right, rect.top, rect.bottom, rect.width, rect.height  
    
    def draw_piece(self, size):
        """Draws the piece based on the provided size """

        # get x/y coords of the piece rect
        left, right, top, bottom, w, h = self.get_dimensions(size)
            
        # if full dark
        if self.type == 0:
            pygame.draw.rect(screen, self.dark_color, (left, top, w, h))
        
        # if full light
        elif self.type == 1:
            pygame.draw.rect(screen, self.light_color, (left, top, w, h))
        
        # if diagonal 
        elif self.type == 2:
        
            diagonal_patterns = {
                "top_left": [(left, top), (right, top), (left, bottom)],  # |*/   
                "top_right": [(left, top), (right, top), (right, bottom)],  # \*|  
                "bottom_right": [(left, bottom), (right, top), (right, bottom)],  # /*|
                "bottom_left": [(left, top), (right, bottom), (left, bottom)],  # |*\
            }

            # ROTATION:
                # 0:  light / dark    ---> 
                # 1:  dark \ light    ---> 
                # 2:  dark / light    --->
                # 3:  light \ dark    ---> 

            rotation_patterns = {
                0: {"light": diagonal_patterns['top_left'], "dark": diagonal_patterns['bottom_right']},  # 0:  light / dark
                1: {"light": diagonal_patterns['top_right'], "dark": diagonal_patterns['bottom_left']},  # 1:  dark \ light
                2: {"light": diagonal_patterns['bottom_right'], "dark": diagonal_patterns['top_left']},  # 2:  dark / light
                3: {"light": diagonal_patterns['bottom_left'], "dark": diagonal_patterns['top_right']},  # 3:  light \ dark   
            }

            # Translate piece rotation type to x,y coords. 
            light_tri = rotation_patterns[self.rotation]["light"]
            dark_tri = rotation_patterns[self.rotation]["dark"]
    
            pygame.draw.polygon(screen, self.light_color, light_tri)
            pygame.draw.polygon(screen, self.dark_color, dark_tri)

    
    def get_dict(self):
        obj_dict = {'type': self.type, 'pos': self.pos, 'rotation': self.rotation, 'light_color': self.light_color, 'dark_color': self.dark_color}
    
        return obj_dict     
    
class Block():
    """
    A Block is a collection of square pieces arranged in a square (count rows = count columns).    
    """


    def __init__(self, rows = 8, cols = 8 , x = 0, y = 0, piece_width = 50, rotation = 0):
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.piece_width = piece_width
        self.rotation = rotation         # default rotation
        self.mirror_type = 2             # TODO: remove hardcoding
        # self.rect = self.create_rect(pos)
        # self.small_rect = self.create_small_rect(pos)

        self.pieces = self.init_block()
        self.width = self.cols * PIECE_WIDTH  # TBD change later 
        self.height = self.rows * PIECE_WIDTH # TBD change later
    
   
    def init_block(self):
         # create an empty 2D list to store pieces:
        pieces = []
        for r in range(self.rows):
            pieces.append([])
            for c in range(self.cols):
                pieces[r].append(None)
                
        return pieces
    
    def mirror_pieces(self):
        """
        Mirrors the pieces set in the top-left quadrant to the other quadrants
        of the block based on the mirror type.
        """
        def _mirror_piece(src_r, src_c, dest_r, dest_c, rotation_adjustment):
            """Helper function to mirror a piece to a new position with adjusted rotation."""
            piece = self.pieces[src_r][src_c]
            new_rotation = piece.rotation if self.mirror_type == 1 else rotation_adjustment[piece.rotation]


            # Piece location is based on block location and what r,c it is in in the block
            x = self.x + (dest_c * self.piece_width)
            y = self.y + (dest_r * self.piece_width)
            
            print(f"Original Piece: r,c: {src_r, src_c} / x,y: {piece.x, piece.y} / type: {piece.type} / Rotation: {piece.rotation}")
            print(f"Mirrored Piece: r,c: {dest_r, dest_c} / x,y: {x, y} / type: {piece.type} / Rotation: {new_rotation}")

            self.pieces[dest_r][dest_c] = Piece(piece.type, new_rotation, x, y, self.piece_width)

        # Define how each quadrant should mirror the top-left quadrant
        quadrant_transforms = [
            # ((new_row, new_col), rotation_map)
            (lambda r, c: (r, self.cols - 1 - c), {0: 1, 1: 0, 2: 3, 3: 2}),  # Top-right
            # (lambda r, c: (self.rows - 1 - r, c), {0: 3, 1: 2, 2: 1, 3: 0}),  # Bottom-left
            # (lambda r, c: (self.rows - 1 - r, self.cols - 1 - c), {0: 2, 1: 3, 2: 0, 3: 1})  # Bottom-right
        ]

        for r in range(self.rows // 2):
            for c in range(self.cols // 2):
                for transform, rotation_map in quadrant_transforms:
                    new_r, new_c = transform(r, c)
                    _mirror_piece(r, c, new_r, new_c, rotation_map)
                
                # ROTATION:
                # 0:  light / dark --> Right: 0->1, Down: 0->3, Downright: 0->2
                # 1:  dark \ light --> Right: 1->0, down: 1->2, downright: 1->3
                # 2:  dark / light --> right: 2->3, down: 2->1, Downright: 2->0
                # 3:  light \ dark --> right: 3->2, Down: 3->0, downright: 3->1
    
    def random_fill(self):
        """
        Fill the top left quadrant of the block with random pieces.
        The top left quadrant will then be mirrored to fill in the rest of the block.
        """
        for r in range(self.rows // 2):
            for c in range(self.cols // 2):
                piece_type = random.choice((0, 1, 2))
                rotation = 1 #random.choice((0, 1, 2, 3))  # Only matters if piece_type == 2

                # Piece location is based on block location and r,c in block
                x = self.x + (c * self.piece_width)
                y = self.y + (r * self.piece_width)

                self.pieces[r][c] = Piece(piece_type, rotation, x, y, self.piece_width)
        
        # fill the rest of the block via the mirroring method
        self.mirror_pieces()


    def update_mirror_type(self, new_mirror_type):
        """
        Updates the mirror type and redraws the block.
        """

        self.mirror_type = new_mirror_type
        self.mirror_pieces()
        self.draw_large_block()  # TODO: update based on design or quilt mode

                
    def draw_large_block(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.pieces[r][c] is None:
                    # Draw an outlined placeholder piece
                    # TODO: maybe have a 'placeholder' Piece type instead and move this logic to the Piece class.
                    x = (c * PIECE_WIDTH) + GRID_OFFSET_X
                    y = (r * PIECE_WIDTH) + GRID_OFFSET_Y
                    pygame.draw.rect(screen, DARK_GRAY, (x, y, PIECE_WIDTH, PIECE_WIDTH), 1)
                else:
                    self.pieces[r][c].draw_piece('regular')

    def draw_quilt_block(self): 
        for r in range(self.rows):
            for c in range(self.cols):
                if self.pieces[r][c] is None:
                    # Draw an outlined placeholder piece
                    # TODO: maybe have a 'placeholder' Piece type instead and move this logic to the Piece class.
                    x = (c * PIECE_WIDTH / 4) + GRID_OFFSET_X
                    y = (r * PIECE_WIDTH / 4) + GRID_OFFSET_Y
                    pygame.draw.rect(screen, DARK_GRAY, (x, y, PIECE_WIDTH, PIECE_WIDTH), 1)
                else:
                    self.pieces[r][c].draw_piece('small')
        

    
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


# def create_color_options(dark_colors, light_colors):
#     # create color objects based on the colors provided
    
#     colors = []
    
#     # for color in dark_colors:
#     for i, color in enumerate(dark_colors):
#         x = (i * OPTIONS_PIECE_WIDTH) + GRID_OFFSET_X
#         y = GRID_OFFSET_Y + BLOCK_WIDTH + (YRES - (GRID_OFFSET_Y + BLOCK_WIDTH))/2  # halfway between bottom of block and bottom
        
#         # create a color object with that color at a unique position
#         new_color = Color(color, 0, (x,y))
#         colors.append(new_color)
        
#     # for color in light_colors:
#     for i, color in enumerate(light_colors):
#         x = (i * OPTIONS_PIECE_WIDTH) + GRID_OFFSET_X
#         y = OPTIONS_PIECE_WIDTH + GRID_OFFSET_Y + BLOCK_WIDTH + (YRES - (GRID_OFFSET_Y + BLOCK_WIDTH))/2  # One row below dark colors
        
#         # create a color object with that color at a unique position
#         new_color = Color(color, 1, (x,y))
#         colors.append(new_color)
        
#     return colors

# def draw_color_options(colors):
    
#     for color in colors:
#         pygame.draw.rect(screen, color.color, color.rect)
        
# def create_piece_options():
#     # create default piece objects 
#     num_piece_options = 3
#     piece_options = []
    
#     for i in range(num_piece_options):

#         x = i  # fake row i (as we're specifying location based on the block now
#         y = 10 # fake col 10
        
#         piece_type = i # 0, 1, 2 for dark, light, diagnoal
        
#         # create a piece object with that color at a unique position
#         new_piece = Piece(piece_type, (x,y))
#         print(new_rect.left)
#         piece_options.append(new_piece)
        
#     return piece_options

# def rotate_piece_options(piece_options):
    
#     for piece in piece_options:
#         if piece.rotation < 3:
#             piece.rotation += 1
#         else:
#             piece.rotation = 0
            
# def update_colors(color_obj, piece_options):
#     for piece in piece_options:
#         if color_obj.color_type == 0:
#             piece.dark_color = color_obj.color
#         if color_obj.color_type == 1:
#             piece.light_color = color_obj.color
    


# def draw_piece_options(piece_options):
#     for piece in piece_options:
#         draw_piece(piece, (0,0), 'regular')
    
  
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
              
# def save_to_json(block, mirror_type):
#     # save block to JSON
#     block_dict = {}
#     piece_dicts = []

#     for r,row in enumerate(block):
#         for col in block[r]:
#             piece_dict = col.get_dict()
#             piece_dicts.append(piece_dict)
    
#     block_dict['mirror'] = mirror_type
#     block_dict['pieces'] = piece_dicts
#     timestr = time.strftime("%Y-%m-%d-%H%M%S")
    
#     with open(f"quilt_block_{timestr}.json", "w") as write_file:
#         json.dump(block_dict, write_file, indent=4) 
    
########################################
# GAME STARTUP
########################################
mode = 'design'
mirror_type = 2
selected_piece_option = None

# the actual block that will hold piece objects
block = Block()

# create dark & light color options
# colors = create_color_options(DARK_COLORS, LIGHT_COLORS)

# create peice options
# piece_options =  create_piece_options() 


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
                # save_to_json(block, mirror_type)   
                pass         
            if event.key == pygame.K_RETURN:
                # random generate top right quarter of block
                block.random_fill()
            if event.key == pygame.K_r:
                # rotate pieces to select from
                # rotate_piece_options(piece_options)
                pass
            if event.key == pygame.K_q:
                if mode == 'design':
                    mode = 'quilt_preview'
                else:
                    mode = 'design'
        
        # if LEFT MOUSE button clicked, check if it collides with anything
        # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
        #     pos = pygame.mouse.get_pos()

        #     # check if cursor is on a color cell. if so update piece option colors.
        #     for color in colors:
        #         if color.rect.collidepoint(pos):
        #             update_colors(color, piece_options)

        #     # check if cursor is on a piece option cell. if so update the selected piece option.
        #     for piece in piece_options:
        #         if rect.collidepoint(pos):
        #             selected_piece_option = piece


        #     # check if cursor is on a piece block piece. if so update the selected piece with the piece option.
        #     for r, row in enumerate(block):
        #         for piece in block[r]:
        #             if piece and rect.collidepoint(pos):
        #                 piece.type = selected_piece_option.type
        #                 piece.rotation = selected_piece_option.rotation
        #                 piece.dark_color = selected_piece_option.dark_color
        #                 piece.light_color = selected_piece_option.light_color
            
                               
            
    if mode == 'design':
        # draw placeholder grid to fill   
        # draw_placeholder_grid()

        # draw dark & light color options
        # draw_color_options(colors)
        
        # draw pieces
        # draw_piece_options(piece_options)

        # if selected_piece_option:
        #     pygame.draw.rect(screen, RED, selected_piece_option.rect, 2)
            
        block.draw_large_block()
        
    if mode == 'quilt_preview':
        # draw_quilt
        draw_quilt(block)
    
  
    
        
            
            
                
    pygame.display.update()
    fpsClock.tick(FPS)