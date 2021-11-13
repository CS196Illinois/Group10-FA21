# import pygame module in this program
import pygame
 
# activate the pygame library
# initiate pygame and give permission
# to use pygame's functionality.
pygame.init()
 
# define the RGB value for white,
#  green, blue colour .
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
 
# assigning values to X and Y variable
X = 400
Y = 400
 
# create the display surface object
# of specific dimension..e(X, Y).
display_surface = pygame.display.set_mode((X, Y))
font = pygame.font.Font('freesansbold.ttf', 32)
 

text = font.render('GeeksForGeeks', True, green, blue)
 

textRect = text.get_rect()

textRect.center = (X // 2, Y // 2)
 
# infinite loop
while True:
 
    # completely fill the surface object
    # with white color
    display_surface.fill(white)
 
    # copying the text surface object
    # to the display surface object
    # at the center coordinate.
    display_surface.blit(text, textRect)
 
    # iterate over the list of Event objects
    # that was returned by pygame.event.get() method.
    for event in pygame.event.get():
 
        # if event object type is QUIT
        # then quitting the pygame
        # and program both.
        if event.type == pygame.QUIT:
 
            # deactivates the pygame library
            pygame.quit()
 
            # quit the program.
            quit()
 
        # Draws the surface object to the screen.
        pygame.display.update()