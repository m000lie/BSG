import pygame

yellow = pygame.image.load("Assets/spaceship_yellow.png")
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(yellow, (55,40)), 90.0)
print(YELLOW_SPACESHIP.get_height(), YELLOW_SPACESHIP.get_width())