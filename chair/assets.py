"""Module for managing assets."""

import pygame
from entities import TILE_SIZE


class AssetManager:
    """A container for managing the loading of assets."""
    def __init__(self):
        self.hero_sprite = load_image("images/hero.png")
        self._terrain_sprite = load_image("images/desert.png")
        xormasks, andmasks = create_cursor()
        self.cursor = CursorData((16, 16), (8, 8), xormasks, andmasks)
        self.terrain_sprites = [
            self._terrain_sprite.subsurface(pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE))
            for x in range(4)
            for y in range(4)
        ]


class CursorData():
    """Simple class for storing all necessary cursor data."""
    def __init__(self, size, hotspot, xormasks, andmasks):
        self.size = size
        self.hotspot = hotspot
        self.xormasks = xormasks
        self.andmasks = andmasks


def create_cursor():
    """generate a cursor in the byzantine format demanded by, I assume, SDL."""
    strings = (
        "       XX       ",
        "      X..X      ",
        "      X..X      ",
        "      X..X      ",
        "      X..X      ",
        "       XX       ",
        " XXXX      XXXX ",
        "X....X    X....X",
        "X....X    X....X",
        " XXXX      XXXX ",
        "       XX       ",
        "      X..X      ",
        "      X..X      ",
        "      X..X      ",
        "      X..X      ",
        "       XX       ")
    return pygame.cursors.compile(
        strings,
        black='X',
        white='.',
        xor='o')


def load_image(path):
    """Load and convert an image from the given path."""
    return pygame.image.load(path).convert_alpha()
