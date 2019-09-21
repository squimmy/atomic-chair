"""Core game loop and logic"""
import random
import math
import pygame
import entities
import assets
import audio
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
    sound_manager = audio.SoundManager()
    projectiles = pygame.sprite.Group()
    projectile_manager = entities.ProjectileManager(
        projectiles,
        clock,
        sound_manager,
        asset_manager.bullet,
        1000)

    hero = entities.Hero(
        100, 200,
        asset_manager.hero_sprite,
        input_manager,
        clock,
        projectile_manager)
    actors = pygame.sprite.Group()
    actors.add(hero)

    terrain = pygame.sprite.Group()
    for x in range(32):
        for y in range(32):
            terrain.add(entities.Terrain(
                x * entities.TILE_SIZE,
                y * entities.TILE_SIZE,
                random.choice(asset_manager.terrain_sprites)))

    baddies = pygame.sprite.Group()
    for i in range(random.randint(5, 8)):
        x = random.randint(0, (640 - entities.TILE_SIZE))
        y = random.randint(0, (480 - entities.TILE_SIZE))
        if math.fabs(x - hero.rect.x) < 64 and math.fabs(y - hero.rect.y) < 64:
            continue
        baddie = entities.Baddie(x, y, asset_manager.goblin)
        baddies.add(baddie)

    while True:
        clock.tick(60)
        input_manager.reset()
        for event in pygame.event.get():
            input_manager.handle_event(event)
            if event.type == pygame.QUIT:
                return
        actors.update()
        projectiles.update()
        terrain.draw(screen)
        actors.draw(screen)
        baddies.draw(screen)
        projectiles.draw(screen)
        pygame.display.flip()


if __name__ == "__main__":
    main()
