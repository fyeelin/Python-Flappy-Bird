import pygame
import sys  # pylint: disable=unused-import
import random  # pylint: disable=unused-import


def main():  # pylint: disable=c0116
    screen = pygame.display.set_mode((288, 512), 0, 32)
    background = pygame.image.load(
        r"D:\python_thing\flapy bird\game soure material\sprites\background-day.png")
    clock = pygame.time.Clock()

    screen.blit(background, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()
