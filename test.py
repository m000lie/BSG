import pygame

# yellow = pygame.image.load("Assets/spaceship_yellow.png")
# YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(yellow, (55,40)), 90.0)
# print(YELLOW_SPACESHIP.get_height(), YELLOW_SPACESHIP.get_width())
while True:
    WIDTH, HEIGHT = 900, 500
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    WIN.fill((255,255,255))
    keys_pressed = pygame.key.get_pressed()

    print(keys_pressed.get)