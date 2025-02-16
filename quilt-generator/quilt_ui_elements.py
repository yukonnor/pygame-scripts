import pygame
from pygame_widgets.button import Button


def create_ui(screen, block, piece_options):
    """Initialize and return UI elements."""

    # Create a button and pass required references
    sync_colors_button = Button(
        screen,
        675,  # X-coordinate
        550,  # Y-coordinate
        100,  # Width
        25,  # Height
        text="Sync Colors",
        fontSize=14,
        margin=8,
        inactiveColour=(200, 50, 0),
        hoverColour=(150, 0, 0),
        pressedColour=(110, 0, 0),
        radius=5,
        onClick=lambda: block.update_piece_colors(
            piece_options[0].light_color, piece_options[0].dark_color
        ),
    )

    return [sync_colors_button]  # Return a list of UI elements for easy management
