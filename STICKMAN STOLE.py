import pygame

def drawMan(screen,x,y):
    #head
    pygame.draw.ellipse(screen,BLACK,[0+x,0+y,10,10], 0)
    #body
    pygame.draw.line(screen,BLACK,[4+x,17+y],[4+x,7+y], 2)
    #legs
    pygame.draw.line(screen,BLACK,[4+x,17+y],[9+x,27+y], 4)
    pygame.draw.line(screen,BLACK,[4+x,17+y],[-1+x,27+y], 4)
    #arms
    pygame.draw.line(screen,BLACK,[4+x,7+y],[8+x,17+y], 2)
    pygame.draw.line(screen,BLACK,[4+x,7+y],[0+x,17+y], 2)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BORDER = (100,100,100)

pygame.init()

size = (800, 500)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Jump")

done = False

clock = pygame.time.Clock()

pygame.mouse.set_visible(1)

xCoord = 11
yCoord = 463

xSpeed = 0
ySpeed = 0

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                xSpeed = -3
            if event.key == pygame.K_RIGHT:
                xSpeed = 3
            if event.key == pygame.K_UP:
                ySpeed = -3

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                xSpeed = 0
            if event.key == pygame.K_RIGHT:
                xSpeed = 0
            if event.key == pygame.K_UP:
                ySpeed = 3


    if xCoord >= 780:
        xSpeed = 0
        xCoord -= 1
    elif xCoord <= 13:
        xSpeed = 0
        xCoord += 1
    elif yCoord > 465:
        ySpeed = 0
        yCoord -= 1
    elif yCoord <= 13:
        ySpeed = 0
        yCoord += 1
    else:
        xCoord += xSpeed
        yCoord += ySpeed


    screen.fill(WHITE)
    pygame.draw.line(screen, BORDER, [0,0],[800,0], 20)
    pygame.draw.line(screen, BORDER, [0,0],[0,500], 20)
    pygame.draw.line(screen, BORDER, [0,500],[800,500], 20)
    pygame.draw.line(screen, BORDER, [800,500],[800,0], 20)


    drawMan(screen,xCoord,yCoord)

    pygame.display.flip()

    clock.tick(60)

pygame.quit()