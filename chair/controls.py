"""Module for handling player input."""

import pygame


class InputManager:
    """Class to aggregate and process input events"""
    def __init__(self):
        self.down_keys = {}
        self.down_buttons = {}
        self.mouse_pos = (0, 0)

    def handle_event(self, event):
        """parse input events to later be converted to actions."""
        if event.type == pygame.KEYDOWN:
            self.down_keys[event.key] = True
        elif event.type == pygame.KEYUP:
            self.down_keys[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.down_buttons[event.button] = True
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.down_buttons[event.button] = False
            self.mouse_pos = event.pos
        elif event.type == pygame.MOUSEMOTION:
            self.mouse_pos = event.pos
        # TODO: gamepad support

    def get_direction(self):
        """Returns a normalized vector of input direction."""
        x = 0
        y = 0
        if self.down_keys.get(pygame.K_a, False):
            x -= 1
        if self.down_keys.get(pygame.K_d, False):
            x += 1
        if self.down_keys.get(pygame.K_w, False):
            y -= 1
        if self.down_keys.get(pygame.K_s, False):
            y += 1
        if x == 0 and y == 0:
            return pygame.math.Vector2(0, 0)
        else:
            return pygame.math.Vector2(x, y).normalize()
