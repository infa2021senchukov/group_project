import pygame

hero_image = pygame.image.load("hero.png").convert()
hero_image.set_colorkey((255, 255, 255)))
wall_image = pygame.image.load("wall.png").convert()

def vis:
    screen.blit(hero_image, [units[0].x, units[0].y])
    screen.blit(wall_image, [units[0].x, units[0].y])