import pygame
import random

pygame.mixer.init()
pygame.init()

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_SPACE,
    RLEACCEL
)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load("Research/dsding/mario.png").convert(), (50, 30))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.y_velocity = 0

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.y_velocity = -10 
        if pressed_keys[K_DOWN]:
            self.y_velocity = 10
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        if pressed_keys[K_SPACE]:
            self.rect.update((150, 150), (75, 25))
        self.rect.move_ip(0, self.y_velocity)
        print(self.y_velocity)
        self.y_velocity += 1

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
            self.y_velocity = 1
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.y_velocity = -1

class Platform(pygame.sprite.Sprite):
    def __init__(self):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((100, 20))
        self.surf.fill((0, 0, 0))
        if(random.randint(0,1) == 0):
            self.movingLeft = True
            self.rect = self.surf.get_rect(
                center=(
                    SCREEN_WIDTH,
                    SCREEN_HEIGHT/2,
                )
            )

        else:
            self.movingLeft = False
            self.rect = self.surf.get_rect(
                center=(
                    0,
                    random.randint(0, SCREEN_HEIGHT),
                )
            )
        self.speed = random.randint(1, 1)
    def update(self):
        if(self.movingLeft):
            self.rect.move_ip(-self.speed, 0)
        else:
            self.rect.move_ip(self.speed, 0)
        if (self.rect.right < -50 or self.rect.left > SCREEN_WIDTH + 50):
            self.kill()

SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_WIDTH])

pygame.mixer.music.load("Research/dsding/bensound-betterdays.mp3")
pygame.mixer.music.play(loops=-1)

platform_sound = pygame.mixer.Sound("Research/dsding/jump.wav")

ADDPLATFORM = pygame.USEREVENT + 1
pygame.time.set_timer(ADDPLATFORM, 2000)

player = Player()

all_platforms = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

clock = pygame.time.Clock()


running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == ADDPLATFORM:
            new_platform = Platform()
            all_platforms.add(new_platform)
            all_sprites.add(new_platform)
    
    pressed_keys = pygame.key.get_pressed()

    screen.fill((255, 255, 255))

    player.update(pressed_keys)

    all_platforms.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    if pygame.sprite.spritecollideany(player, all_platforms):
        player.y_velocity = -40
        platform_sound.play()

    pygame.display.flip()

    clock.tick(30)

pygame.mixer.music.stop()
pygame.mixer.quit()


