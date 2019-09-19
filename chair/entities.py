"""Game entities."""
import math
import pygame
from pygame import Rect

TILE_SIZE = 32


class Hero(pygame.sprite.Sprite):
    """The player-controlled actor."""
    def __init__(self, x, y, image, input_manager, clock):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.input_manager = input_manager
        self.clock = clock
        self.inertia = pygame.math.Vector2()
        self.speed = 0.17

    def update(self):
        """Update the player position depending on player input. sub-pixel
        pixel positioning isn't supported, so input is stored in a vector
        so that fractional input can be aggregated over multiple frames."""
        input_vector = self.input_manager.get_direction()
        input_vector *= self.clock.get_time() * self.speed
        self.inertia += input_vector
        while math.fabs(self.inertia.x) >= 1:
            self.rect.x += self.inertia.x
            self.inertia.x -= math.copysign(1, self.inertia.x)
        while math.fabs(self.inertia.y) >= 1:
            self.rect.y += self.inertia.y
            self.inertia.y -= math.copysign(1, self.inertia.y)


class Terrain(pygame.sprite.Sprite):
    """Simple sprite for terrain and environment."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
