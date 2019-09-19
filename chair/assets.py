"""Module for managing assets."""

import pygame
from entities import TILE_SIZE


class AssetManager:
    """A container for managing the loading of assets."""
    def __init__(self):
        self.hero_sprite = load_image("images/hero.png")
        self._terrain_sprite = load_image("images/desert.png")
        self.terrain_sprites = [
            self._terrain_sprite.subsurface(pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE))
            for x in range(4)
            for y in range(4)
        ]


def load_image(path):
    """Load and convert an image from the given path."""
    return pygame.image.load(path).convert_alpha()
