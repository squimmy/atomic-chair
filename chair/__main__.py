"""Core game loop and logic"""
import random
import pygame
import entities
import assets


def main():
    """Initialise the game and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    asset_manager = assets.AssetManager()
    hero = entities.Hero(100, 200, asset_manager.hero_sprite)
    actors = pygame.sprite.Group()
    actors.add(hero)

    terrain = pygame.sprite.Group()
    for x in range(32):
        for y in range(32):
            terrain.add(entities.Terrain(
                x * entities.TILE_SIZE,
                y * entities.TILE_SIZE,
                random.choice(asset_manager.terrain_sprites)))

    while True:
        terrain.draw(screen)
        actors.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == "__main__":
    main()
