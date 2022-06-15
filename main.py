import pygame
import os

pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Battlestar Galactica")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
RESULT_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
SHIP_SCALE = (55, 40)
VELOCITY = 5
BULLET_VELOCITY = 10
AMMO = 3
'''
Pygame has a total of 32 event slots (ID’s), of which the first 23 are used by Pygame (pre-defined events). 
Event ID’s from 24 to 32 are available for our use.
The pygame.USEREVENT has a value of 24, which we can assign to our user-defined event. 
For creating a second event, you would do pygame.USEREVENT + 1 (for an ID of 25), and so on.
'''
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, SHIP_SCALE), 90.0)

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, SHIP_SCALE), 270.0)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    """This is to draw the window environment.

    Args:
        red (pygame.Rect() object): Red spaceship
        yellow (pygame.Rect() object): Yellow spaceship
        red_bullets (List[pygame.Rect()]): List of pygame.Rect() objects for red spaceship bullets
        yellow_bullets (List[pygame.Rect()]): List of pygame.Rect() objects for yellow spaceship bullets
        red_health (int): Red Spaceship Health
        yellow_health (int): Yellow Spaceship Health
    """
    # WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    pygame.display.update()


def yellow_movement_handler(keys_pressed, yellow):  # LEFT
    """Movement handler for yellow spaceship

    Args:
        keys_pressed (List[bool]): List of bools representing the state of every key
        yellow (pygame.Rect()): Yellow spaceship pygame.Rect() object
    """
    if keys_pressed[pygame.K_a] and (yellow.x - VELOCITY) > 0:  # LEFT
        if keys_pressed[pygame.K_LSHIFT]:  # SPRINT
            yellow.x -= VELOCITY + 1
        yellow.x -= VELOCITY

    if keys_pressed[pygame.K_d] and (yellow.x + VELOCITY) < 405:  # RIGHT
        if keys_pressed[pygame.K_LSHIFT]:  # SPRINT
            yellow.x += VELOCITY + 1
        yellow.x += VELOCITY

    if keys_pressed[pygame.K_w] and (yellow.y - VELOCITY) > 0:  # UP
        if keys_pressed[pygame.K_LSHIFT]:  # SPRINT
            yellow.y -= VELOCITY + 1
        yellow.y -= VELOCITY

    if keys_pressed[pygame.K_s] and (yellow.y + VELOCITY) < 440:  # DOWN
        if keys_pressed[pygame.K_LSHIFT]:  # SPRINT
            yellow.y += VELOCITY + 1
        yellow.y += VELOCITY


def red_movement_handler(keys_pressed, red):  # RIGHT
    if keys_pressed[pygame.K_LEFT] and (red.x - VELOCITY) > 455:  # LEFT
        if keys_pressed[pygame.K_RSHIFT]:  # SPRINT
            red.x -= VELOCITY + 1
        red.x -= VELOCITY

    if keys_pressed[pygame.K_RIGHT] and (red.x + VELOCITY) < 860:  # RIGHT
        if keys_pressed[pygame.K_RSHIFT]:  # SPRINT
            red.x += VELOCITY + 1
        red.x += VELOCITY

    if keys_pressed[pygame.K_UP] and (red.y - VELOCITY) > 0:  # UP
        if keys_pressed[pygame.K_RSHIFT]:  # SPRINT
            red.y -= VELOCITY + 1
        red.y -= VELOCITY

    if keys_pressed[pygame.K_DOWN] and (red.y + VELOCITY) < 440:  # DOWN
        if keys_pressed[pygame.K_RSHIFT]:  # SPRINT
            red.y += VELOCITY + 1
        red.y += VELOCITY


# handle bullet collision, movement, bullet going off-screen
def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        if (bullet.x - BULLET_VELOCITY) > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VELOCITY
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        if (bullet.x - BULLET_VELOCITY) < 0:
            red_bullets.remove(bullet)


def draw_result(text):
    draw_text = RESULT_FONT.render(text, True, WHITE)
    WIN.blit(draw_text,
             ((WIDTH // 2) - (draw_text.get_width() // 2), (HEIGHT // 2) - (draw_text.get_height() // 2)), )
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    yellow = pygame.Rect(100, 300, 55, 40)
    red = pygame.Rect(700, 300, 55, 40)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # BULLETS
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LSUPER and len(yellow_bullets) < AMMO:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + ((yellow.height // 2) - 2), 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSUPER and len(red_bullets) < AMMO:
                    bullet = pygame.Rect(red.x, red.y + ((red.height // 2) - 2), 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()


            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        # calculate result
        if (red_health + yellow_health) == 0:
            result_text = "It's a tie!"
            draw_result(result_text)
            pygame.quit()
            break
        if red_health <= 0:
            result_text = "Yellow wins!"
            draw_result(result_text)
            pygame.quit()
            break
        if yellow_health <= 0:
            result_text = "Red wins!"
            draw_result(result_text)
            pygame.quit()
            break

        # print(f"YELLOW FIRED: {len(yellow_bullets)}, RED FIRED: {len(red_bullets)}")
        # print(yellow_bullets, red_bullets)

        # movement_controllers
        keys_pressed = pygame.key.get_pressed()
        yellow_movement_handler(keys_pressed, yellow)
        red_movement_handler(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()


if __name__ == "__main__":
    main()
