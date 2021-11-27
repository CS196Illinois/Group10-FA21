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


PLAYER_MOVE_SPEED = 8

dirname = os.path.dirname(__file__)

class Player(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos, controlDict):
        super(Player, self).__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join(dirname, "playerSprite.png")).convert(), (20,50))
        self.rect = self.surf.get_rect(center = (xPos, yPos))
        self.dx, self.dy = 0, 0
        self.touchingPlatform = False
        self.score = 0
        self.controlDict = controlDict
        self.power = False
        self.bulletNumber = 1.0
        self.lastKey = True
                

    def update(self, pressed_keys, possibleCollisionSprites):
        self.moving = False
        
        if self.bulletNumber < 0.3*self.score + 1:
            self.bulletNumber += 0.001*self.score + 0.005
        if pressed_keys[self.controlDict["jump"]] and self.touchingPlatform:
            self.dy = -20
        if pressed_keys[self.controlDict["down"]]:
            #debug float, replace with groundpound later
            self.dy = 5
        if pressed_keys[self.controlDict["left"]]:
            self.moving = True
            if self.dx > PLAYER_MOVE_SPEED * -1:
                if self.touchingPlatform:
                    self.dx -= 2
                else:
                    self.dx -= 1
            self.lastKey = False
        if pressed_keys[self.controlDict["right"]]:
            self.moving = True
            if self.dx < PLAYER_MOVE_SPEED:
                if self.touchingPlatform:
                    self.dx += 2
                else:
                    self.dx += 1
            self.lastKey = True
        #resets character position for demo
        if pressed_keys[self.controlDict["power"]]:
            if self.bulletNumber > 1 :
                if self.lastKey == True:
                    AddBullet(self.rect[0] + 20, self.rect[1])
                    self.bulletNumber -= 1
                if self.lastKey == False:
                    AddLeftBullet(self.rect[0] - 20, self.rect[1])
                    self.bulletNumber -= 1
        if pressed_keys[K_SPACE]:
            self.dx = 0
            self.dy = 0
            self.rect.center = (0,0)
            self.score = 0
            killCoin()
            AddCoin()
        #deceleration/friction
        if self.touchingPlatform and not self.moving:
            self.dx = 0

        for coin in pygame.sprite.spritecollide(self, coin_sprites, True, collided = None):
            self.score += 1
            coin.kill()
            print(self.score)

        for power in pygame.sprite.spritecollide(self, power_sprites, True, collided = None):
            self.power = True
            power.kill()
            print(self.power)

        for bullet in pygame.sprite.spritecollide(self, bullet_sprites, True, collided = None):
            self.dx += 25
            bullet.kill()
            print("success")

        for leftBullet in pygame.sprite.spritecollide(self, leftBullet_sprites, True, collided = None):
            self.dx -= 25
            leftBullet.kill()
            print("success")
        
        
        self.dy += 1

        self.collidedCharacter = pygame.sprite.spritecollide(self, possibleCollisionSprites, False)

        # cool collision detection below here
        self.oldrect = self.rect.copy()
        #steps forward one tick of movement and sees if there is a collision then
        self.rect.move_ip(self.dx,self.dy)
        self.collidedList = pygame.sprite.spritecollide(self, possibleCollisionSprites, False)
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
    def __init__(self, xPos, yPos):
        super(Coin, self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (255,255,0), (15, 15), 15)

class Power(pygame.sprite.Sprite):
    def __init__(self, xPos, yPos):
        super(Power, self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (255,100,30), (15, 15), 10)

class Bullet(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (25,150,30), (20, 20), 5)

    def update(self):
        self.rect[0] += 20

class LeftBullet(pygame.sprite.Sprite):

    def __init__(self, xPos, yPos):
        super(LeftBullet, self).__init__()
        self.surf = pygame.Surface((30,30))
        self.surf.set_colorkey((0,0,0))
        self.rect = self.surf.get_rect(
            left = xPos,
            top = yPos
        )
        pygame.draw.circle(self.surf, (25,150,30), (20, 20), 5)

    def update(self):
        self.rect[0] -= 20

    
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
    
    def update(self, pressed_keys, possibleCollisionSprites):
        for bullet in pygame.sprite.spritecollide(self, bullet_sprites, True, collided = None):
            print("success")
        for leftbullet in pygame.sprite.spritecollide(self, leftBullet_sprites, True, collided = None):
            print("success")

# helper function that creates a new platform and adds it to the needed sprite groups
def newPlatform(xPos, yPos, xSize, ySize):
    myPlatform = Platform(xPos, yPos, xSize, ySize)
    solid_sprites.add(myPlatform)
    all_sprites.add(myPlatform)

def newCoin(xPos, yPos):
    myCoin = Platform(xPos, yPos)
    coin_sprites.add(myCoin)
    all_sprites.add(myCoin)
    
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

# (xpos, ypos, xsize, ysize): xpos, ypos represents coordinates of the top left corner

# "Standard" width of platform
pw = 50

# player 1 start location
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

# create Coin instances
# this part of code is not elegent, but I do not know how to make it better...
# later, replace this with some way to randomly generate coins
coin_sprites = pygame.sprite.Group()
power_sprites = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
leftBullet_sprites = pygame.sprite.Group()
platform_sprites = pygame.sprite.Group()
def AddCoin():
    coin1 = Coin(190,460)
    all_sprites.add(coin1)
    coin2 = Coin(275,80)
    all_sprites.add(coin2)
    coin3 = Coin(335,80)
    all_sprites.add(coin3)
    coin4 = Coin(215,80)
    all_sprites.add(coin4)
    coin5 = Coin(410,230)
    all_sprites.add(coin5)
    coin6 = Coin(470,230)
    all_sprites.add(coin6)
    coin7 = Coin(530,230)
    all_sprites.add(coin7)
    coin8 = Coin(350,230)
    all_sprites.add(coin8)
    coin9 = Coin(885,320)
    all_sprites.add(coin9)
    coin10 = Coin(945,320)
    all_sprites.add(coin10)
    coin11 = Coin(575,400)
    all_sprites.add(coin11)
    coin12 = Coin(515,400)
    all_sprites.add(coin12)
    coin13 = Coin(635,400)
    all_sprites.add(coin13)
    coin14 = Coin(885,500)
    all_sprites.add(coin14)
    coin15 = Coin(945,500)
    all_sprites.add(coin15)
    coin16 = Coin(1005,500)
    all_sprites.add(coin16)
    # L shape
    coin17 = Coin(250,560)
    all_sprites.add(coin17)
    coin18 = Coin(310,560)
    all_sprites.add(coin18)
    coin19 = Coin(890,100)
    all_sprites.add(coin19)
    coin20 = Coin(950,100)
    all_sprites.add(coin20)
    coin21 = Coin(830,100)
    all_sprites.add(coin21)
    coin22 = Coin(870,200)
    all_sprites.add(coin22)
    coin_sprites.add(coin1)
    coin_sprites.add(coin2)
    coin_sprites.add(coin3)
    coin_sprites.add(coin4)
    coin_sprites.add(coin5)
    coin_sprites.add(coin6)
    coin_sprites.add(coin7)
    coin_sprites.add(coin8)
    coin_sprites.add(coin9)
    coin_sprites.add(coin10)
    coin_sprites.add(coin11)
    coin_sprites.add(coin12)
    coin_sprites.add(coin13)
    coin_sprites.add(coin14)
    coin_sprites.add(coin15)
    coin_sprites.add(coin16)
    coin_sprites.add(coin17)
    coin_sprites.add(coin18)
    coin_sprites.add(coin19)
    coin_sprites.add(coin20)
    coin_sprites.add(coin21)
    coin_sprites.add(coin22)

def AddPower():
    power1 = Power(250,460)
    all_sprites.add(power1)
    power_sprites.add(power1)

def AddBullet(dx, dy):
    bullet1 = Bullet(dx,dy)
    all_sprites.add(bullet1)
    bullet_sprites.add(bullet1)
    bullet1.update()

def AddLeftBullet(dx, dy):
    bullet1 = LeftBullet(dx,dy)
    all_sprites.add(bullet1)
    leftBullet_sprites.add(bullet1)
    bullet1.update()

AddCoin()
AddPower()

def killCoin():
    for item in coin_sprites:
        item.kill()

#move_up_sound = pygame.mixer.Sound("ao.ogg")
#move_down_sound = pygame.mixer.Sound("ao.ogg")

#move_up_sound.set_volume(1)
#move_down_sound.set_volume(1)


def text_objects(text, font):
    textSurface = font.render(text, True, (0,0,0))
    return textSurface, textSurface.get_rect()

def message_display(text, xpos, ypos):
    largeText = pygame.font.Font('freesansbold.ttf',20)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (xpos,ypos)
    screen.blit(TextSurf, TextRect)





running = True


while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False


    pressed_keys = pygame.key.get_pressed()

    player1.update(pressed_keys, solid_sprites)
    player2.update(pressed_keys, solid_sprites)
    bullet_sprites.update()
    leftBullet_sprites.update()
    solid_sprites.update(pressed_keys, solid_sprites)


    screen.fill((200, 200, 200))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    message_display("Player1 Score: " +str(player1.score), 100, 50)
    message_display("Player2 Score: " +str(player2.score), 1180, 50)
    pygame.display.flip()

    clock.tick(60)