"""
TODO:
- Add ability to load patterns
- Different mirror types
- Different block -> quilt fill types
- Multi-block quilt
- Very pieces per block / blocks per quilt & scale accordingly
- Multi-size pieces
"""

import pygame
import time
import pygame_widgets
from colors import *

from quilt_constants import (
    PIECE_WIDTH,
    BLOCK_POS_OFFSET,
    DARK_COLORS,
    LIGHT_COLORS,
    SCREEN_BG_COLOR,
)
from models import Piece, Block, Color, JSONEncoder
from quilt_ui_elements import create_ui  # Import UI elements


pygame.init()
DEBUG = True

# determin speed of animation
FPS = 30
fpsClock = pygame.time.Clock()

# screen size
XRES = 800
YRES = 800

FONT = pygame.font.SysFont("retrogaming", 16)
FONT_BIG = pygame.font.SysFont("retrogaming", 24)
FONT_HUGE = pygame.font.SysFont("retrogaming", 48)

screen = pygame.display.set_mode((XRES, YRES))

###############################################################################
###############################################################################


def create_color_options(dark_colors, light_colors):
    # create color objects based on the colors provided

    color_options = []
    color_options_block_location = (BLOCK_POS_OFFSET, YRES - (BLOCK_POS_OFFSET / 2))

    # for color in dark_colors:
    for i, color in enumerate(dark_colors):
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
        piece.draw(screen)


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
# GAME SETUP
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

# create UI elements
ui_elements = create_ui(screen, block, piece_options)


########################################
# Main Game Loop
########################################
while True:
    screen.fill(BLACK)

    # events & quit
    events = pygame.event.get()
    for event in events:
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

            if event.key == pygame.K_i:
                block.invert_colors()

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

            if event.key == pygame.K_z:
                block.update_mirror_type(0)
            if event.key == pygame.K_x:
                block.update_mirror_type(1)
            if event.key == pygame.K_c:
                block.update_mirror_type(2)

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
        block.draw_design_mode(screen)

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

            pygame_widgets.update(events)  # draw all UI elements

    if mode == "quilt_preview":

        block.draw_quilt_mode(screen, 5, 4)

    pygame.display.update()
    fpsClock.tick(FPS)
