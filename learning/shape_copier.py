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

XRES = 400
YRES = 400

XMID = XRES/2
YMID = YRES/2


gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(BLACK)

# scetch constants
COUNT_COPIES = 9                    # in addition to the base shape
MAX_DISTANCE_X = (XRES - XMID) / 2  # max distance copies can be away from main object
MAX_DISTANCE_Y = (YRES - YMID) / 2
SHAPE_SIZE = 50
SHOW_BORDER = True
SHOW_FILL = True

color_start = (255, 255, 255)         # color of base shape
color_end = (255,0,0)                 # color of furthest shape

draw_direction = 1 # 1: 'Top2Bottom', 2: 'Bottom2Top

# create shapes
shapes = ['Rect', 'Circle', 'Triangle']
baseRect = pygame.Rect(0,0,SHAPE_SIZE,SHAPE_SIZE) # rect at center of screen
baseRect.center = (XMID, YMID) # rect at center of screen
additionalRect = []

for i in range(COUNT_COPIES):
    additionalRect.append(pygame.Rect(baseRect))

# main game loop
while True:
    gameDisplay.fill(BLACK)     # clear screen 

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # get randomized position for farest Rect
    x_max = random.randint(XMID - MAX_DISTANCE_X, XMID + MAX_DISTANCE_X)
    y_max = random.randint(YMID - MAX_DISTANCE_Y, YMID + MAX_DISTANCE_Y)

    # variables to calculate Rect coordinates
    x_dif = x_max - XMID
    y_dif = y_max - YMID
    x_step = x_dif / COUNT_COPIES
    y_step = y_dif / COUNT_COPIES

    # varibales to calculate colors
    r0, g0, b0 = color_start
    r1, g1, b1 = color_end
    r_step = int((r1-r0)/COUNT_COPIES)
    g_step = int((g1-g0)/COUNT_COPIES)
    b_step = int((b1-b0)/COUNT_COPIES)    

    if draw_direction == 1:
        # draw furthest shape first so it's at bottom
        
        # calculate Rect coordinates & draw
        for i in range(COUNT_COPIES):
            additionalRect[i].centerx = x_max - (x_step * i)
            additionalRect[i].centery = y_max - (y_step * i)

            r = r1 - (r_step * i)
            g = g1 - (g_step * i)
            b = b1 - (b_step * i) 
            
            if SHOW_FILL:
                pygame.draw.rect(gameDisplay,(r,g,b),additionalRect[i])  # draw fill
            if SHOW_BORDER:
                pygame.draw.rect(gameDisplay,BLACK,additionalRect[i],1)  # draw outline
            

        # draw center shape last
        if SHOW_FILL: 
            pygame.draw.rect(gameDisplay,color_start,baseRect)
        if SHOW_BORDER:
            pygame.draw.rect(gameDisplay,BLACK,baseRect,1)
    
    elif draw_direction == 2:
        # draw center shape first (at bottom)
        if SHOW_FILL:
            pygame.draw.rect(gameDisplay,color_start,baseRect)
        if SHOW_BORDER:
                pygame.draw.rect(gameDisplay,BLACK,baseRect,1)  # draw outline

        # calculate Rect coordinates & colors and draw
        for i in range(COUNT_COPIES):
            additionalRect[i].centerx = baseRect.centerx + (x_step * i)
            additionalRect[i].centery = baseRect.centery + (y_step * i)

            r = r0 + (r_step * i)
            g = g0 + (g_step * i)
            b = b0 + (b_step * i) 

            if SHOW_FILL:
                pygame.draw.rect(gameDisplay,(r,g,b),additionalRect[i])
            if SHOW_BORDER:
                pygame.draw.rect(gameDisplay,BLACK,additionalRect[i],1)  # draw outline
        
            
    
    sleep(.2)
    pygame.display.update()

    fpsClock.tick(FPS)