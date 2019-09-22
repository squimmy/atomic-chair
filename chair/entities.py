"""Game entities."""
import pygame
from pygame import Rect
from pygame.math import Vector2

TILE_SIZE = 32


class Motile(pygame.sprite.Sprite):
    """Any sprite capable of movement."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.pos = pygame.math.Vector2(x, y)
        self._offset_x = self.image.get_width() / 2
        self._offset_y = self.image.get_height() / 2
        self.rect = Rect(
            x - self._offset_x,
            y - self._offset_y,
            self.image.get_width(),
            self.image.get_height())

    def update_position(self, vec):
        """Update the position of the sprite and align the image to it."""
        self.pos.update(vec)
        self.rect.x = self.pos.x - self._offset_x
        self.rect.y = self.pos.y - self._offset_y


class Hero(Motile):
    """The player-controlled actor."""
    def __init__(self, x, y, image, input_manager,
                 clock, projectile_manager):
        Motile.__init__(self, x, y, image)
        self.input_manager = input_manager
        self.clock = clock
        self.speed = 0.25
        self.projectile_manager = projectile_manager

    def update(self):
        """Update the player position depending on player input. sub-pixel
        pixel positioning isn't supported, so input is stored in a vector
        so that fractional input can be aggregated over multiple frames."""
        input_vector = self.input_manager.get_direction()
        input_vector *= self.clock.get_time() * self.speed
        self.update_position(self.pos + input_vector)
        if self.input_manager.clicked_buttons[1]:
            target = Vector2(self.input_manager.mouse_pos)
            direction = target - self.pos
            direction.scale_to_length(0.5)
            self.projectile_manager.add_bullet(
                self.pos.x,
                self.pos.y,
                direction)


class Baddie(pygame.sprite.Sprite):
    """Base class for baddies."""
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = Rect(x, y, TILE_SIZE, TILE_SIZE)


class Projectile(Motile):
    """A projectile that will move in a straight line for a specified time."""
    def __init__(self, x, y, image, velocity, lifetime, clock):
        Motile.__init__(self, x, y, image)
        self.velocity = velocity
        self.lifetime = lifetime
        self.clock = clock

    def update(self):
        """Move the projectile and reduce its lifespan."""
        delta_t = self.clock.get_time()
        self.lifetime -= delta_t
        if self.lifetime <= 0:
            self.kill()
        motion = self.velocity * delta_t
        self.update_position(self.pos + motion)


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
