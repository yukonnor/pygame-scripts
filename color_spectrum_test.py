import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from colors import *         # import the color variables from local file
from pygame import gfxdraw

pygame.init()  

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

HRES = 400
VRES = 400

X_MID = HRES/2
Y_MID = VRES/2


gameDisplay = pygame.display.set_mode((HRES,VRES))
gameDisplay.fill(BLACK)


# draw background lines
line_count = 80  # one verticle line every 5 pixels
line_color_start = (50, 168, 82)
line_color_end = (255,0,0)
for i in range(line_count):
    pygame.draw.line(gameDisplay, WHITE, (i*5,0), (i*5,VRES),1)


# main game loop
while True:
    gameDisplay.fill(BLACK)     # clear screen 

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # draw lines
    r0, g0, b0 = line_color_start
    r1, g1, b1 = line_color_end
    r = r0
    g = g0
    b = b0

    for i in range(line_count):
        r += (r1-r0)/line_count
        g += (g1-g0)/line_count
        b += (b1-b0)/line_count
        pygame.draw.line(gameDisplay, (r,g,b), (i*5,0), (i*5,VRES),2)
        pygame.draw.line(gameDisplay, (r,g,b), (0,i*5), (HRES,i*5),2)


    pygame.display.update()

    fpsClock.tick(FPS)


'''
NOTES:

- It's possible to draw lines with points outside the game display boundary

'''