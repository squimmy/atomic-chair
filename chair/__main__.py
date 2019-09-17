"""Core game loop and logic"""
import pygame
import entities


def main():
    """Initialise the game and run the main game loop."""
    pygame.init()
    screen = pygame.display.set_mode((640, 480))

    hero_sprite = pygame.image.load("images/hero.png")
    hero = entities.Hero(100, 200, hero_sprite)
    actors = pygame.sprite.Group()
    actors.add(hero)

    while True:
        actors.draw(screen)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return


if __name__ == "__main__":
    main()
