"""Module for handling player input."""

from collections import defaultdict
import pygame


class InputManager:
    """Class to aggregate and process input events"""
    def __init__(self):
        self.down_keys = defaultdict(lambda: False)
        self.down_buttons = defaultdict(lambda: False)
        self.clicked_buttons = defaultdict(lambda: False)
        self.mouse_pos = (0, 0)

    def reset(self):
        """Call this each frame to reset the input manager state."""
        for key in self.clicked_buttons.keys():
            self.clicked_buttons[key] = False

    def handle_event(self, event):
        """parse input events to later be converted to actions."""
        if event.type == pygame.KEYDOWN:
            self.down_keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.down_keys[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.clicked_buttons[event.button] = True
            self.down_buttons[event.button] = True
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            self.down_buttons[event.button] = False
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        # TODO: gamepad support

    def get_direction(self):
        """Returns a normalized vector of input direction."""
        x = 0
        y = 0
        if self.down_keys[pygame.K_a]:
            x -= 1
        if self.down_keys[pygame.K_d]:
            x += 1
        if self.down_keys[pygame.K_w]:
            y -= 1
        if self.down_keys[pygame.K_s]:
            y += 1
        if x == 0 and y == 0:
            return pygame.math.Vector2(0, 0)
        else:
            return pygame.math.Vector2(x, y).normalize()
