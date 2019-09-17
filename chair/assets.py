"""Module for managing assets."""

import pygame
from entities import TILE_SIZE


class AssetManager:
    """A container for managing the loading of assets."""
    def __init__(self):
        self.hero_sprite = pygame.image.load("images/hero.png").convert_alpha()
        self._terrain_sprite = pygame.image.load("images/desert.png").convert_alpha()
        self.terrain_sprites = [
            self._terrain_sprite.subsurface(pygame.Rect(
                x * TILE_SIZE,
                y * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE))
            for x in range(4)
            for y in range(4)
        ]
