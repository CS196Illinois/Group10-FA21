import pygame
pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.rect.update((150, 150), (75, 25))

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_WIDTH])

player = Player()

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pressed_keys = pygame.key.get_pressed()

    # Fill the background with white
    screen.fill((255, 255, 255))

    # Draw a solid black circle in the center
    # pygame.draw.circle(screen, (0, 0, 0), (250, 250), 75)
    player.update(pressed_keys)
    screen.blit(player.surf, player.rect)

    pygame.display.flip()



