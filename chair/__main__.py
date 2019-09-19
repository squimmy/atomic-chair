"""Core game loop and logic"""
import random
import pygame
import entities
import assets
import controls


def main():
    """Initialise the game and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    input_manager = controls.InputManager()

    asset_manager = assets.AssetManager()
    pygame.mouse.set_cursor(
        asset_manager.cursor.size,
        asset_manager.cursor.hotspot,
        asset_manager.cursor.xormasks,
        asset_manager.cursor.andmasks)
    clock = pygame.time.Clock()

    hero = entities.Hero(
        100, 200,
        asset_manager.hero_sprite,
        input_manager,
        clock)
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
        clock.tick(60)
        for event in pygame.event.get():
            input_manager.handle_event(event)
            if event.type == pygame.QUIT:
                return
        actors.update()
        terrain.draw(screen)
        actors.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
