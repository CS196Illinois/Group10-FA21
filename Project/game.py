import pygame

import random

import os

import sys


from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    K_SPACE,
    QUIT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_f,
    K_p
    

)
from pygame.sprite import spritecollide

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
coinSpawnEvent = 0 + pygame.USEREVENT
powerSpawnEvent = 1 + pygame.USEREVENT

PLAYER_MOVE_SPEED = 4

dirname = os.path.dirname(__file__)

class Player(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos, controlDict):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join(dirname, "playerSprite.png")).convert(), (20,50))
        self.start = (xPos, yPos)
        self.rect = self.surf.get_rect(center = self.start)
        self.dx, self.dy = 0, 0
        self.touchingPlatform = False
        self.score = 0
        self.controlDict = controlDict
        self.power = "none"
        self.facingRight = True
                

    def update(self, pressed_keys):
        self.moving = False
        
        if pressed_keys[self.controlDict["jump"]] and self.touchingPlatform:
            self.dy = -11
        #if pressed_keys[self.controlDict["down"]]:
            #Make this a groundpound or something
        if pressed_keys[self.controlDict["left"]]:
            self.moving = True
            if self.dx > PLAYER_MOVE_SPEED * -1:
                if self.touchingPlatform:
                    self.dx -= .5
                else:
                    self.dx -= .25
            self.facingRight = False
        if pressed_keys[self.controlDict["right"]]:
            self.moving = True
            if self.dx < PLAYER_MOVE_SPEED:
                if self.touchingPlatform:
                    self.dx += .5
                else:
                    self.dx += .25
            self.facingRight = True
        if pressed_keys[self.controlDict["power"]]:
            if self.power == "bullet" :
                if self.facingRight == True:
                    bullet = Bullet(self.rect[0] + 30, self.rect[1], 20)
                if self.facingRight == False:
                    bullet = Bullet(self.rect[0] - 30, self.rect[1], -20)
                all_sprites.add(bullet)
                bullet_sprites.add(bullet)
                self.power = "none"
        #deceleration/friction
        if self.touchingPlatform and not self.moving:
            self.dx = 0
        
        if self.rect.centery > SCREEN_HEIGHT + 400:
            self.rect.center = self.start
            self.score = max((0, self.score - 10))
            self.dx, self.dy = 0, 0

        for coin in pygame.sprite.spritecollide(self, coin_sprites, True, collided = None):
            self.score += 1
            coin.kill()

        for power in pygame.sprite.spritecollide(self, power_sprites, True):
            self.power = power.power
            power.kill()
            print("touched power")

        for bullet in pygame.sprite.spritecollide(self, bullet_sprites, True):
            self.dx += bullet.speed * .7
            self.dy -= 12
            self.score = max((0, self.score - 10))
            bullet.kill()
 
        self.dy += .25

        self.collidedCharacter = pygame.sprite.spritecollide(self, solid_sprites, False)

        # cool collision detection below here
        self.oldrect = self.rect.copy()
        #steps forward one tick of movement and sees if there is a collision then
        self.rect.move_ip(self.dx,self.dy)
        self.collidedList = pygame.sprite.spritecollide(self, solid_sprites, False)
        self.collidedList.remove(self) #prevent the player from colliding with itself
        self.touchingPlatform = False

        #if there are collisions, you need to push the player out of those future collisions now
        #this might have buggy results if multiple platforms are collided or have contradicting pushouts
        for collidedSprite in self.collidedList:
            #check if player is directly above or below other sprite
            #we use oldrect for comparison to prevent pushing into the sides causing the square to jump to the top
            if collidedSprite.rect.left < self.oldrect.right and collidedSprite.rect.right > self.oldrect.left:

                #if player is above collided sprite
                if collidedSprite.rect.top < self.rect.bottom and collidedSprite.rect.bottom > self.rect.bottom:
                    self.rect.move_ip(0, collidedSprite.rect.top - self.rect.bottom) #push out of platform
                    self.dy = 0
                    self.touchingPlatform = True
            
                #if player is below collided sprite
                elif collidedSprite.rect.bottom > self.rect.top and collidedSprite.rect.top < self.rect.top:
                    self.rect.move_ip(0, collidedSprite.rect.bottom - self.rect.top)
                    self.dy = 0
            
            #check if player is mainly left or right of other sprite
            if collidedSprite.rect.top < self.rect.bottom and collidedSprite.rect.bottom > self.rect.top:
                
                #if player is left of collided sprite
                if collidedSprite.rect.left < self.rect.right and collidedSprite.rect.left > self.rect.left:
                    self.rect.move_ip(collidedSprite.rect.left - self.rect.right, 0)
                    self.dx = 0
                
                #if player is right of collided sprite
                elif collidedSprite.rect.right > self.rect.left and collidedSprite.rect.right < self.rect.right:
                    self.rect.move_ip(collidedSprite.rect.right - self.rect.left, 0)
                    self.dx = 0

        
class Coin(pygame.sprite.Sprite):
    width = 30
    def __init__(self, xPos, yPos):
        super(Coin, self).__init__()
        self.surf = pygame.Surface((Coin.width, Coin.width))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (255,255,0), (Coin.width//2, Coin.width//2), Coin.width//2)

class Power(pygame.sprite.Sprite):
    width = 20
    def __init__(self, xPos, yPos):
        super(Power, self).__init__()
        self.surf = pygame.Surface((Power.width, Power.width))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (255,100,30), (Power.width//2, Power.width//2), Power.width//2)
        self.power = "none"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, speed):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (25,150,30), (20, 20), 5)
        self.speed = speed

    def update(self):
        self.rect[0] += self.speed

class Platform(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos, xSize, ySize):
        super(Platform, self).__init__()
        self.surf = pygame.Surface((xSize,ySize))
        self.surf.set_colorkey((0,0,1), RLEACCEL)
        self.rect = self.surf.get_rect(
        left = xPos,
        top = yPos
    )
        pygame.draw.rect(self.surf, (168, 17, 0), pygame.Rect(2, 2, self.rect.width - 4, self.rect.height - 4))
        for i in range(8, self.rect.height - 2, 15):
            pygame.draw.rect(self.surf, (87, 9, 0), pygame.Rect(2, i, self.rect.width - 4, 5))    
    
    def update(self, pressed_keys):
        pygame.sprite.spritecollide(self, bullet_sprites, True, collided = None)
            

# helper function that creates a new platform and adds it to the needed sprite groups
def newPlatform(xPos, yPos, xSize, ySize):
    myPlatform = Platform(xPos, yPos, xSize, ySize)
    solid_sprites.add(myPlatform)
    all_sprites.add(myPlatform)

def newRandomSpawn(Type):
    #subtract 4 b/c there are 4 solid sprites to never spawn coins on (players and start platforms)
    pos = random.random() * (len(solid_sprites) - 4)
    platform = solid_sprites.sprites()[int(pos) + 4]
    # 40 is arbitrary
    newItem = Type(platform.rect.left + ((platform.rect.width-Type.width) * (pos - int(pos))), platform.rect.top - 40)
    if not spritecollide(newItem, all_sprites, False):
        if (Type == Power):
            newItem.power = "bullet"
            power_sprites.add(newItem)
            print("power spawned")
        else:
            coin_sprites.add(newItem)
        all_sprites.add(newItem)


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text, xpos, ypos):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (xpos,ypos)
    screen.blit(TextSurf, TextRect)   
 
pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# player control dictonary, mapping an action to a keypress
p1ControlDict = {
    "jump": K_w,
    "left": K_a,
    "down": K_s,
    "right": K_d,
    "power": K_f
}
p2ControlDict = {
    "jump": K_UP,
    "left": K_LEFT,
    "down": K_DOWN,
    "right": K_RIGHT,
    "power": K_p
}

player1 = Player(50, 50, p1ControlDict)
player2 = Player(SCREEN_WIDTH - 50, 50, p2ControlDict)


all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)


#solid means that players cannot overlap that object (players should be solid to each other)
solid_sprites = pygame.sprite.Group()
solid_sprites.add(player1)
solid_sprites.add(player2)

coin_sprites = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()

# "Standard" width of platform
pw = 50

# player 1 start location
# platform 1
newPlatform(30, 300, pw * 2, pw)

# player 2 start location
newPlatform(SCREEN_WIDTH - 30 - (pw * 2), 300, pw * 2, pw)

# flat platforms
newPlatform(200, 120, pw * 4, pw)
newPlatform(340, 270, pw * 5, pw)
newPlatform(500, 440, pw * 4, pw)
newPlatform(870, 540, pw * 4, pw)
newPlatform(890, 360, pw * 2, pw)

# L platform 1
newPlatform(190, 500, pw, pw * 3)
newPlatform(190, 500 + (pw * 2), pw * 4, pw)

# L platform 2
newPlatform(810, 140 + pw, pw, pw * 1)
newPlatform(810, 140, pw * 4, pw)

for i in range(20):
    newRandomSpawn(Coin)
pygame.time.set_timer(coinSpawnEvent, 200)
pygame.time.set_timer(powerSpawnEvent, 1)

running = True

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        if event.type == coinSpawnEvent:
            newRandomSpawn(Coin)
            pygame.time.set_timer(coinSpawnEvent, random.randint(200, 400))
        if event.type == powerSpawnEvent:
            newRandomSpawn(Power)
            pygame.time.set_timer(powerSpawnEvent, random.randint(16000, 30000))


    pressed_keys = pygame.key.get_pressed()

    bullet_sprites.update()
    solid_sprites.update(pressed_keys)

    screen.fill((200, 200, 200))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    message_display("Player1 Score: " +str(player1.score), 100, 50)
    message_display("Power: " + player1.power, 100, 100)

    message_display("Player2 Score: " +str(player2.score), 1180, 50)
    message_display("Power: " + player2.power, 1180, 100)
    pygame.display.flip()

    clock.tick(60)