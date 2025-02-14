"""
This sketch:

TODO:
- Add ability to load patterns
- fill block with different colors
- Different mirror types
- Edit block
- Weighted random for piece selection
- CLEAN UP code

"""

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
PIECE_WIDTH = 50  # TODO make scale
BLOCK_POS_OFFSET = 200
QUILT_SCALE = 125 / 400  #  Size of quilt block / Size of design block
OPTIONS_PIECE_WIDTH = 50
GRID_OFFSET_X = (XRES - (PIECE_WIDTH * 8)) / 2
GRID_OFFSET_Y = (YRES - (PIECE_WIDTH * 8)) / 2

FONT = pygame.font.SysFont("retrogaming", 16)
FONT_BIG = pygame.font.SysFont("retrogaming", 24)
FONT_HUGE = pygame.font.SysFont("retrogaming", 48)

DARK_COLORS = (
    "#085FA5",
    "#3E5F2E",
    "#212221",
    "#343330",
    "#DC851F",
    "#172A3A",
    "#D63B26",
    "#540B0E",
)
LIGHT_COLORS = ("#FFFBE3", "#FFF3B0", "#E09F3E", "#FFA737", "#74D63F", "#A0D8FF")

screen = pygame.display.set_mode((XRES, YRES))

###############################################################################
###############################################################################


class Piece:
    def __init__(
        self,
        type=0,
        rotation=0,
        block_coords=(0, 0),
        block_pos=(0, 0),
        width=PIECE_WIDTH,
        dark_color=DARK_COLORS[0],
        light_color=LIGHT_COLORS[0],
    ):
        self.type = type  # 0,1,2,3 for placeholder, full_dark, full_light or diag
        self.rotation = rotation  # default rotation
        self.block_coords = block_coords  # (x,y) coordinates of parent block
        self.block_pos = block_pos  # (r,c) position within paren block
        self.width = width  # Width is determined based on parent structure.
        self.dark_color = dark_color  # default dark color
        self.light_color = light_color  # default light color

        # Define the default rect:
        self.rect = self.create_rect()
        # self.small_rect = self.create_small_rect()

        # a piece's x,y position is based on its location in the block's 2D array. It depends on the block position.
        # a block's x,y position is based on its location in the quilt's 2D array.

        # ROTATION:
        # 0:  light / dark
        # 1:  dark \ light
        # 2:  dark / light
        # 3:  light \ dark

    def create_rect(self):
        """define the rect position based on the block position the piece is in"""
        x = self.block_coords[0] + (self.block_pos[1] * self.width)
        y = self.block_coords[1] + (self.block_pos[0] * self.width)
        return pygame.Rect(x, y, self.width, self.width)

    # def create_small_rect(self):
    #     """ 1/4 of regular size, for quilt mode """
    #     x = self.block_coords[0] + (self.block_pos[1] * self.width * QUILT_SCALE)
    #     y = self.block_coords[1] + (self.block_pos[0] * self.width * QUILT_SCALE)
    #     return pygame.Rect(x, y, self.width * QUILT_SCALE, self.width * QUILT_SCALE)

    def draw(self, provided_rect=None):
        """Draw the piece based on the provided rect"""

        # If rect provided, use it. Otherwise use default rect.
        rect = provided_rect if provided_rect else self.rect

        # Extract coordinates from the rectangle
        left, right, top, bottom, w, h = (
            rect.left,
            rect.right,
            rect.top,
            rect.bottom,
            rect.width,
            rect.height,
        )

        # if placeholder
        if self.type == 0:
            pygame.draw.rect(
                screen, DARK_GRAY, (left, top, w, h), 1
            )  # outlined empty square

        # if full dark
        if self.type == 1:
            pygame.draw.rect(screen, self.dark_color, (left, top, w, h))

        # if full light
        elif self.type == 2:
            pygame.draw.rect(screen, self.light_color, (left, top, w, h))

        # if diagonal
        elif self.type == 3:

            diagonal_patterns = {
                "top_left": [(left, top), (right, top), (left, bottom)],  # |*/
                "top_right": [(left, top), (right, top), (right, bottom)],  # \*|
                "bottom_right": [(left, bottom), (right, top), (right, bottom)],  # /*|
                "bottom_left": [(left, top), (right, bottom), (left, bottom)],  # |*\
            }

            rotation_patterns = {
                0: {
                    "light": diagonal_patterns["top_left"],
                    "dark": diagonal_patterns["bottom_right"],
                },  # 0:  light / dark
                1: {
                    "light": diagonal_patterns["top_right"],
                    "dark": diagonal_patterns["bottom_left"],
                },  # 1:  dark \ light
                2: {
                    "light": diagonal_patterns["bottom_right"],
                    "dark": diagonal_patterns["top_left"],
                },  # 2:  dark / light
                3: {
                    "light": diagonal_patterns["bottom_left"],
                    "dark": diagonal_patterns["top_right"],
                },  # 3:  light \ dark
            }

            # Translate piece rotation type to x,y coords.
            light_tri = rotation_patterns[self.rotation]["light"]
            dark_tri = rotation_patterns[self.rotation]["dark"]

            pygame.draw.polygon(screen, self.light_color, light_tri)
            pygame.draw.polygon(screen, self.dark_color, dark_tri)

    def draw_at(self, x, y, draw_mode="design"):
        """Draw the piece at a specific temporary location."""

        # Calculate the width based on the draw mode, ensuring integer values
        size = (
            round(self.width)
            if draw_mode == "design"
            else round(self.width * QUILT_SCALE)
        )

        # Create a temporary rectangle for drawing with rounded coordinates
        temp_rect = pygame.Rect(round(x), round(y), size, size)

        # Pass the temp_rect to the draw function
        self.draw(temp_rect)

    def get_dict(self):
        obj_dict = {
            "type": self.type,
            "pos": self.pos,
            "rotation": self.rotation,
            "light_color": self.light_color,
            "dark_color": self.dark_color,
        }

        return obj_dict


class Block:
    """
    A Block is a collection of square pieces arranged in a square (count rows = count columns).

    A block is displayed to the user in two ways:
     - Block design mode (default)
     - Quilt mode (where the block is scaled smaller - currently hard-coded to 1/4 the size).

    This allows edits to the block's pieces update the entire quilt w/o having to go into the quilt and update each block copy.
    """

    def __init__(self, rows=8, cols=8, x=0, y=0, piece_width=50):
        self.rows = rows
        self.cols = cols
        self.x = x
        self.y = y
        self.piece_width = piece_width
        self.mirror_type = 2  # TODO: remove hardcoding

        self.pieces = self.init_block()  # create an empty 2D array to store pieces
        self.rand_rotation_options = [0, 1, 2, 3]
        self.width = self.cols * piece_width
        self.height = self.rows * piece_width

    def init_block(self):
        # create an empty 2D list to store pieces:
        pieces = []
        for r in range(self.rows):
            pieces.append([])
            for c in range(self.cols):
                pieces[r].append(
                    Piece(0, 0, (self.x, self.y), (r, c))
                )  # Create 'placeholder' Piece

        return pieces

    def mirror_pieces(self):
        """
        Mirrors the pieces set in the top-left quadrant to the other quadrants
        of the block based on the mirror type.
        """

        def _mirror_piece(src_r, src_c, dest_r, dest_c, rotation_adjustment):
            """Helper function to mirror a piece to a new position with adjusted rotation."""
            piece = self.pieces[src_r][src_c]
            new_rotation = (
                piece.rotation
                if self.mirror_type == 1
                else rotation_adjustment[piece.rotation]
            )

            self.pieces[dest_r][dest_c] = Piece(
                piece.type,
                new_rotation,
                (self.x, self.y),
                (dest_r, dest_c),
                dark_color=piece.dark_color,
                light_color=piece.light_color,
            )

        # Define how each quadrant should mirror the top-left quadrant
        quadrant_transforms = [
            # ((new_row, new_col), rotation_map)
            (
                lambda r, c: (r, self.cols - 1 - c),
                {0: 1, 1: 0, 2: 3, 3: 2},
            ),  # Top-right
            (
                lambda r, c: (self.rows - 1 - r, c),
                {0: 3, 1: 2, 2: 1, 3: 0},
            ),  # Bottom-left
            (
                lambda r, c: (self.rows - 1 - r, self.cols - 1 - c),
                {0: 2, 1: 3, 2: 0, 3: 1},
            ),  # Bottom-right
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

    def random_fill(self, dark_color, light_color):
        """
        Fill the top left quadrant of the block with random pieces, based on current color settings of piece_option blocks
        The top left quadrant will then be mirrored to fill in the rest of the block.
        """
        for r in range(self.rows // 2):
            for c in range(self.cols // 2):
                piece_type = random.choice((1, 2, 3))
                rotation = random.choice(self.rand_rotation_options)

                self.pieces[r][c] = Piece(
                    piece_type,
                    rotation,
                    (self.x, self.y),
                    (r, c),
                    dark_color=dark_color,
                    light_color=light_color,
                )

        # fill the rest of the block via the mirroring method
        self.mirror_pieces()

    def update_mirror_type(self, new_mirror_type):
        """
        Updates the mirror type and redraws the block.
        """
        pass

    def draw_design_mode(self):
        """Draw a large single block for editing."""
        for row in self.pieces:
            for piece in row:
                piece_x = self.x + piece.block_pos[1] * piece.width
                piece_y = self.y + piece.block_pos[0] * piece.width
                piece.draw_at(piece_x, piece_y, draw_mode="design")

    def draw_quilt_mode(self, quilt_rows, quilt_cols):
        """Draws multiple smaller copies of this block to form a repeating quilt pattern."""
        quilt_x = 150
        quilt_y = 100

        for qr in range(quilt_rows):
            for qc in range(quilt_cols):
                block_x = quilt_x + (qc * self.width * QUILT_SCALE)
                block_y = quilt_y + (qr * self.width * QUILT_SCALE)

                for row in self.pieces:
                    for piece in row:
                        piece_x = (
                            block_x + piece.block_pos[1] * piece.width * QUILT_SCALE
                        )
                        piece_y = (
                            block_y + piece.block_pos[0] * piece.width * QUILT_SCALE
                        )
                        piece.draw_at(piece_x, piece_y, draw_mode="quilt")


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        obj_dict = {
            "type": obj.type,
            "pos": obj.pos,
            "rotation": obj.rotation,
            "light_color": obj.light_color,
            "dark_color": obj.dark_color,
        }

        return obj_dict


class Color:
    def __init__(self, color, color_type, pos):
        self.pos = pos  # (xres, yres)
        self.color = color
        self.color_type = color_type  # 'dark' or 'light'
        self.rect = pygame.Rect(self.pos[0], self.pos[1], PIECE_WIDTH, PIECE_WIDTH)


###############################################################################
###############################################################################


def create_color_options(dark_colors, light_colors):
    # create color objects based on the colors provided

    color_options = []
    color_options_block_location = (BLOCK_POS_OFFSET, YRES - (BLOCK_POS_OFFSET / 2))

    # for color in dark_colors:
    for i, color in enumerate(dark_colors):
        print(color)
        x = color_options_block_location[0] + (i * PIECE_WIDTH)
        y = color_options_block_location[1]

        # create a color object with that color at a unique position
        new_color = Color(color, "dark", (x, y))
        color_options.append(new_color)

    # for color in light_colors:
    for i, color in enumerate(light_colors):
        x = color_options_block_location[0] + (i * PIECE_WIDTH)
        y = color_options_block_location[1] + PIECE_WIDTH  # one row below dark colors

        # create a color object with that color at a unique position
        new_color = Color(color, "light", (x, y))
        color_options.append(new_color)

    return color_options


def draw_color_options(color_options):

    for color in color_options:
        pygame.draw.rect(screen, color.color, color.rect)


def create_piece_options():
    # create default piece objects
    num_piece_options = 6
    piece_options = []

    piece_options_block_location = (XRES - (BLOCK_POS_OFFSET / 2), BLOCK_POS_OFFSET)

    for i in range(num_piece_options):
        # Create the two solid block types:
        if i < 2:
            type = i + 1
            rotation = 0
            new_piece = Piece(type, rotation, piece_options_block_location, (i, 0))
        # Create the four diagonal block types
        else:
            type = 3
            rotation = i - 2
            new_piece = Piece(type, rotation, piece_options_block_location, (i, 0))

        piece_options.append(new_piece)

    return piece_options


def update_piece_option_colors(color_obj, piece_options):
    for piece in piece_options:
        if color_obj.color_type == "dark":
            piece.dark_color = color_obj.color
        if color_obj.color_type == "light":
            piece.light_color = color_obj.color


def draw_piece_options(piece_options):
    for piece in piece_options:
        piece.draw()


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
mode = "design"
mirror_type = 2
selected_piece_option = None

# Instantiate the Block that will hold quilt Pieces
block = Block()
block.x, block.y = BLOCK_POS_OFFSET, BLOCK_POS_OFFSET

# Bool to show or hide the design tools (color options, piece options)
show_design_tools = True

# create color options
color_options = create_color_options(DARK_COLORS, LIGHT_COLORS)

# create peice options
piece_options = create_piece_options()


########################################
# Main Game Loop
########################################
while True:
    screen.fill(BLACK)  # clear screen

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
                dark_color = piece_options[0].dark_color
                light_color = piece_options[0].light_color

                block.random_fill(dark_color, light_color)

            if event.key == pygame.K_0:
                # limit the rotation to the "0" orientation when random filling
                block.rand_rotation_options = [0]
            if event.key == pygame.K_1:
                # limit the rotation to the "1" orientation when random filling
                block.rand_rotation_options = [1]
            if event.key == pygame.K_2:
                # limit the rotation to the "2" orientation when random filling
                block.rand_rotation_options = [2]
            if event.key == pygame.K_3:
                # limit the rotation to the "3" orientation when random filling
                block.rand_rotation_options = [3]
            if event.key == pygame.K_4:
                # allow all orientations when random filling
                block.rand_rotation_options = [0, 1, 2, 3]

            if event.key == pygame.K_d:
                show_design_tools = not show_design_tools

            if event.key == pygame.K_q:
                if mode == "design":
                    mode = "quilt_preview"
                else:
                    mode = "design"

        # if LEFT MOUSE button clicked, check if it collides with anything
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pos = pygame.mouse.get_pos()
            piece_clicked = False

            # check if cursor is on a color cell. if so update piece option colors.
            for color in color_options:
                if color.rect.collidepoint(pos):
                    update_piece_option_colors(color, piece_options)
                    piece_clicked = True

            # check if cursor is on a piece option cell. if so update the selected piece option.
            for piece in piece_options:
                if piece.rect.collidepoint(pos):
                    selected_piece_option = piece
                    piece_clicked = True

            # check if cursor is on a block piece. if so update the selected piece with the piece option.
            if selected_piece_option:
                for row in block.pieces:
                    for piece in row:
                        if piece.rect.collidepoint(pos):
                            piece.type = selected_piece_option.type
                            piece.rotation = selected_piece_option.rotation
                            piece.dark_color = selected_piece_option.dark_color
                            piece.light_color = selected_piece_option.light_color
                            piece_clicked = True

            # if click didn't collide with anything, deselect the selected piece option
            if not piece_clicked:
                selected_piece_option = None

    if mode == "design":
        # draw the main block
        block.draw_design_mode()

        # draw the design options
        if show_design_tools:
            draw_piece_options(piece_options)

            if selected_piece_option:
                selection_rect = pygame.Rect(
                    selected_piece_option.rect.left - 2,
                    selected_piece_option.rect.top - 2,
                    selected_piece_option.rect.width + 4,
                    selected_piece_option.rect.height + 4,
                )
                pygame.draw.rect(screen, YELLOW, selection_rect, 2)

            draw_color_options(color_options)

    if mode == "quilt_preview":

        block.draw_quilt_mode(5, 4)

    pygame.display.update()
    fpsClock.tick(FPS)
