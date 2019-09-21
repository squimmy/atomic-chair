"""Game entities."""
import math
import pygame
from pygame import Rect
from pygame.math import Vector2

TILE_SIZE = 32


class Hero(pygame.sprite.Sprite):
    """The player-controlled actor."""
    def __init__(self, x, y, image, input_manager,
                 clock, projectiles, bullet_factory):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.input_manager = input_manager
        self.clock = clock
        self.inertia = pygame.math.Vector2()
        self.speed = 0.17
        self.projectiles = projectiles
        self.bullet_factory = bullet_factory

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
        if self.input_manager.clicked_buttons[1]:
            target_x, target_y = self.input_manager.mouse_pos
            rel_x = target_x - self.rect.x
            rel_y = target_y - self.rect.y
            direction = Vector2(rel_x, rel_y)
            direction.scale_to_length(0.25)
            bullet = self.bullet_factory.make_bullet(
                self.rect.x,
                self.rect.y,
                direction)
            self.projectiles.add(bullet)


class Projectile(pygame.sprite.Sprite):
    """A projectile that will move in a straight line for a specified time."""
    def __init__(self, x, y, image, velocity, lifetime, clock):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.velocity = velocity
        self.lifetime = lifetime
        self.clock = clock
        self.inertia = pygame.math.Vector2()

    def update(self):
        """Move the projectile and reduce its lifespan."""
        delta_t = self.clock.get_time()
        self.lifetime -= delta_t
        if self.lifetime <= 0:
            self.kill()
        motion = self.velocity * delta_t
        self.inertia += motion
        while math.fabs(self.inertia.x) >= 1:
            self.rect.x += self.inertia.x
            self.inertia.x -= math.copysign(1, self.inertia.x)
        while math.fabs(self.inertia.y) >= 1:
            self.rect.y += self.inertia.y
            self.inertia.y -= math.copysign(1, self.inertia.y)


class BulletFactory:
    """Class to simplify the creation of bullets."""
    def __init__(self, clock, default_image, default_lifetime):
        self.clock = clock
        self.default_image = default_image
        self.default_lifetime = default_lifetime

    def make_bullet(self, x, y, velocity, image=None, lifetime=None):
        """Create a default bullet."""
        img = image or self.default_image
        life = lifetime or self.default_lifetime
        return Projectile(x, y, img, velocity, life, self.clock)


class Terrain(pygame.sprite.Sprite):
    """Simple sprite for terrain and environment."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)
