import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from colors import *         # import the color variables from local file
from pygame import gfxdraw
import random
from time import sleep

pygame.init()  

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

XRES = 800  
YRES = 600

XMID = XRES/2
YMID = YRES/2

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(BLACK)

# GLOBAL VARIABLES
NUM_POINTS = 5
x_coords = [40,41,42,43,44]
y_coords = [40,41,42,43,44]

dx = 1
dy = 1


def move_dots():

    global dx
    global dy
       
    x_coords[0] = x_coords[0]+(3*dx)
    x_coords[1] = x_coords[1]+(4*dx)
    x_coords[2] = x_coords[2]+(5*dx)
    x_coords[3] = x_coords[3]+(6*dx)
    x_coords[4] = x_coords[4]+(7*dx)
    if x_coords[4] <= 40 or x_coords[4] >= XRES-40:
        dx = -1 * dx


    y_coords[1] = y_coords[1]+dy
    y_coords[2] = y_coords[2]+(2*dy)
    y_coords[3] = y_coords[3]+(3*dy)
    y_coords[4] = y_coords[4]+(4*dy)
    if y_coords[4] <= 40 or y_coords[4] >= YRES-40:
        dy = -1 * dy 


def draw_pixels():

    square_size = 8

    for i in range(NUM_POINTS):
        for j in range(NUM_POINTS):
            # draw square #1:
            rect_1 = pygame.Rect(x_coords[i], y_coords[j], square_size, square_size)
            pygame.draw.rect(gameDisplay, (255,255,255,100), rect_1)

            # draw square #2:
            rect_2 = pygame.Rect((XRES - x_coords[i]),(YRES - y_coords[j]), square_size, square_size)
            pygame.draw.rect(gameDisplay, WHITE, rect_2)

            # draw square #3: 
            rect_3 = pygame.Rect((XRES - x_coords[i]), y_coords[j], square_size, square_size) 
            pygame.draw.rect(gameDisplay, WHITE, rect_3)

            # draw square #4:
            rect_4 = pygame.Rect(x_coords[i], (YRES - y_coords[j]), square_size, square_size)
            pygame.draw.rect(gameDisplay, WHITE, rect_4)
    
def fill_frame_buffer(surface):
    buffer = surface.copy()
    buffer.set_alpha(200)         # alpha level (0-255)
    return(buffer)


def draw_frame_buffer(surface, location = (0,0)):
    gameDisplay.blit(surface,location)


'''
draw screen
get copy of what's on screen
adjust it to add transparency
clear screen
draw that copy onto the screen
'''

frame_count = 0


# main game loop
while True:
    gameDisplay.fill(BLACK)     # clear screen 
    
    if frame_count > 0:
        draw_frame_buffer(buffer)

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    move_dots()
    draw_pixels()
    buffer = fill_frame_buffer(gameDisplay)
    
    #sleep(.2)
    pygame.display.update()

    fpsClock.tick(FPS)
    frame_count += 1