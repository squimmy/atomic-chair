"""Game entities."""
import math
import pygame
from pygame import Rect
from pygame.math import Vector2

TILE_SIZE = 32


class Hero(pygame.sprite.Sprite):
    """The player-controlled actor."""
    def __init__(self, x, y, image, input_manager,
                 clock, projectile_manager):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.input_manager = input_manager
        self.clock = clock
        self.pos = Vector2(x, y)
        self.speed = 0.25
        self.projectile_manager = projectile_manager

    def update(self):
        """Update the player position depending on player input. sub-pixel
        pixel positioning isn't supported, so input is stored in a vector
        so that fractional input can be aggregated over multiple frames."""
        input_vector = self.input_manager.get_direction()
        input_vector *= self.clock.get_time() * self.speed
        self.pos += input_vector
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        if self.input_manager.clicked_buttons[1]:
            center_x, center_y = self._get_center()
            target_x, target_y = self.input_manager.mouse_pos
            rel_x = target_x - center_x
            rel_y = target_y - center_y
            direction = Vector2(rel_x, rel_y)
            direction.scale_to_length(0.5)
            self.projectile_manager.add_bullet(center_x, center_y, direction)

    def _get_center(self):
        return (self.rect.x + TILE_SIZE / 2,
                self.rect.y + TILE_SIZE / 2)


class Baddie(pygame.sprite.Sprite):
    """Base class for baddies."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)


class Projectile(pygame.sprite.Sprite):
    """A projectile that will move in a straight line for a specified time."""
    def __init__(self, x, y, image, velocity, lifetime, clock):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(
            x - image.get_width() / 2,
            y - image.get_height() / 2,
            TILE_SIZE,
            TILE_SIZE)
        self.velocity = velocity
        self.lifetime = lifetime
        self.clock = clock
        self.pos = pygame.math.Vector2(x, y)

    def update(self):
        """Move the projectile and reduce its lifespan."""
        delta_t = self.clock.get_time()
        self.lifetime -= delta_t
        if self.lifetime <= 0:
            self.kill()
        motion = self.velocity * delta_t
        self.pos += motion
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y


class ProjectileManager:
    """Class to simplify the handling of projectiles."""
    def __init__(self,
                 projectiles,
                 clock,
                 sound_manager,
                 bullet_image,
                 bullet_lifetime):
        self.projectiles = projectiles
        self.clock = clock
        self.sound_manager = sound_manager
        self.bullet_image = bullet_image
        self.bullet_lifetime = bullet_lifetime

    def add_bullet(self, x, y, velocity, image=None, lifetime=None):
        """Create a default bullet and add it to the projectile group."""
        img = image or self.bullet_image
        life = lifetime or self.bullet_lifetime
        self.projectiles.add(Projectile(x, y, img, velocity, life, self.clock))
        self.sound_manager.play_shoot()


class Terrain(pygame.sprite.Sprite):
    """Simple sprite for terrain and environment."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
