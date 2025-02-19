import pygame
from pygame_widgets.button import Button, ButtonArray


def create_ui(screen, block, piece_options):
    """Initialize and return UI elements."""

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

    mirror_type_button = ButtonArray(
        screen,
        655,  # X-coordinate
        600,  # Y-coordinate
        120,  # Width
        25,  # Height
        (4, 1),  # Shape: 4 buttons wide, 1 buttons tall
        texts=("0", "1", "2", "3"),
        border=0,
        colour=(200, 50, 0),
        onClicks=(
            lambda: block.update_mirror_type(0),
            lambda: block.update_mirror_type(1),
            lambda: block.update_mirror_type(2),
            lambda: block.update_mirror_type(3),
        ),
    )

    return [
        sync_colors_button,
        mirror_type_button,
    ]  # Return a list of UI elements for easy management
