import pygame
import random
import json

from quilt_constants import (
    PIECE_WIDTH,
    QUILT_SCALE,
    DARK_COLORS,
    LIGHT_COLORS,
    SCREEN_BG_COLOR,
)


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

    def draw(self, screen, provided_rect=None):
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
                screen, SCREEN_BG_COLOR, (left, top, w, h), 1
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

    def draw_at(self, screen, x, y, draw_mode="design"):
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
        self.draw(screen, temp_rect)

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
        self.mirror_type = 2  # Available: 0, 1

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
            new_rotation = rotation_adjustment[piece.rotation]

            self.pieces[dest_r][dest_c] = Piece(
                piece.type,
                new_rotation,
                (self.x, self.y),
                (dest_r, dest_c),
                dark_color=piece.dark_color,
                light_color=piece.light_color,
            )

        # Define how each quadrant should mirror the top-left quadrant
        mirror_type_transformations = [
            [
                # Mirror Type 0 (duplicate): ((new_row, new_col), rotation_map)
                (
                    lambda r, c: (r, c + self.cols // 2),  # Top-right
                    {0: 0, 1: 1, 2: 2, 3: 3},
                ),
                (
                    lambda r, c: (r + self.rows // 2, c),  # Bottom-left
                    {0: 0, 1: 1, 2: 2, 3: 3},
                ),
                (
                    lambda r, c: (
                        r + self.rows // 2,
                        c + self.cols // 2,
                    ),  # Bottom-right
                    {0: 0, 1: 1, 2: 2, 3: 3},
                ),
            ],
            [
                # Mirror Type 1 (classic mirror): ((new_row, new_col), rotation_map)
                (
                    lambda r, c: (r, self.cols - 1 - c),  # Top-right
                    {0: 1, 1: 0, 2: 3, 3: 2},
                ),
                (
                    lambda r, c: (self.rows - 1 - r, c),  # Bottom-left
                    {0: 3, 1: 2, 2: 1, 3: 0},
                ),
                (
                    lambda r, c: (self.rows - 1 - r, self.cols - 1 - c),  # Bottom-right
                    {0: 2, 1: 3, 2: 0, 3: 1},
                ),
            ],
            [
                # Mirror Type 2 (vertical mirror): ((new_row, new_col), rotation_map)
                (
                    lambda r, c: (r, self.cols - 1 - c),  # Top-right
                    {0: 1, 1: 0, 2: 3, 3: 2},
                ),
                (
                    lambda r, c: (r + self.rows // 2, c),  # Bottom-left  (TL)
                    {0: 0, 1: 1, 2: 2, 3: 3},
                ),
                (
                    # Bottom-right (TR)
                    lambda r, c: (
                        r + self.rows // 2,
                        self.cols - 1 - c,
                    ),
                    {0: 1, 1: 0, 2: 3, 3: 2},
                ),
            ],
        ]

        for r in range(self.rows // 2):
            for c in range(self.cols // 2):
                for transform, rotation_map in mirror_type_transformations[
                    self.mirror_type
                ]:
                    new_r, new_c = transform(r, c)
                    _mirror_piece(r, c, new_r, new_c, rotation_map)

                # Mirror Type 1 ROTATION:
                # 0:  light / dark --> Right: 0->1, Down: 0->3, Downright: 0->2
                # 1:  dark \ light --> Right: 1->0, down: 1->2, downright: 1->3
                # 2:  dark / light --> right: 2->3, down: 2->1, Downright: 2->0
                # 3:  light \ dark --> right: 3->2, Down: 3->0, downright: 3->1

    def update_mirror_type(self, new_mirror_type):
        """
        Updates the mirror type and redraws the block.
        """
        self.mirror_type = new_mirror_type
        self.mirror_pieces()

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

    def invert_colors(self):
        """Inverts the colors of the block pieces, keeping the same block design."""
        for row in self.pieces:
            for piece in row:
                og_light_color = piece.light_color
                piece.light_color = piece.dark_color
                piece.dark_color = og_light_color

    def update_piece_colors(self, new_light_color, new_dark_color):
        """Updates the colors of all of the pieces in the block."""
        for row in self.pieces:
            for piece in row:
                piece.light_color = new_light_color
                piece.dark_color = new_dark_color

    def draw_design_mode(self, screen):
        """Draw a large single block for editing."""
        for row in self.pieces:
            for piece in row:
                piece_x = self.x + piece.block_pos[1] * piece.width
                piece_y = self.y + piece.block_pos[0] * piece.width
                piece.draw_at(screen, piece_x, piece_y, draw_mode="design")

    def draw_quilt_mode(self, screen, quilt_rows, quilt_cols):
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
                        piece.draw_at(screen, piece_x, piece_y, draw_mode="quilt")


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
