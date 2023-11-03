'''
Draw a series of rows that each contain rectangles with random width

GENERATE
To start, each row shoud have a rect starting at (0,row_location) and should be random(5,20) long.
Then, draw another rect 5 spaces to the right, also random(5,20) long.
Keep doing so until the starting point of the next rect is > XRES.
Then move to draw the next row of rectangles.

ANIMATE
Move each rect left or right based on the `speed`.
Once a rect is fully off screen, remove it.
Once there is a gap next to a rect, draw a new rect
'''

import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors import *         # import the color variables from local file
from pygame import gfxdraw
import random

pygame.init()  

# determin speed of animation
FPS = 20                       
fpsClock = pygame.time.Clock() 

XRES = 400
YRES = 300

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(BLACK)

# initial values for global variables
rect_height = 6
v_buffer = 4
h_buffer = 4
min_width = 5
max_width = 20
row_height = rect_height + v_buffer
row_count = int(YRES/row_height)
speed = 1


# generate coordinates of rects
def gen_init_rect_coords():
    rects = []# rects[row][(rect_#,rect_widt)] = [[(0,5),(9,21)],]
    for i in range(row_count):
        row_of_rects = []

        for j in range(40):     # high amount of loops to cover case of random picking a lot of small #s
            
            if j == 0:
                x_pos = random.randint(-5,5)
                width = random.randint(min_width,max_width)
            else:
                x_prev,w_prev = row_of_rects[j-1]
                #print(x_prev,w_prev)
                x_pos = x_prev + w_prev + h_buffer
                width = random.randint(min_width,max_width)
            
            if x_pos > XRES:
                break
            else:
                row_of_rects.append([x_pos,width])
        
        rects.append(row_of_rects)
    
    return rects

# move rects
def move_rects(rect_list, speed):
    if speed == 0:
        pass
    elif speed > 0:
        for row in range(len(rect_list)):
            for rect_data in rects[row]:
                # if the first rect is > 0, draw another rect before it
                # it should be placed between max_width + h_buff - min_width + h_buff before the first rect
                # its width should be (first rect - h_buff) - new_rect_placement
                rect_data[0] += speed
                if rect_data[0] > XRES:
                    # remove the last rect to 
                    rect_list[row].pop()

    elif speed < 0:
        for row in range(len(rect_list)):
            for rect_data in rects[row]:
                rect_data[0] -= speed

# BEFORE LOOP STARTS:

# gen rect coords
rects = gen_init_rect_coords()

# MAIN LOOP
while True:

    gameDisplay.fill(BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # determine if any arrow key was pressed
            if event.key == pygame.K_SPACE:
                pass
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_1]:
        rect_height += 1
    if keys[pygame.K_2]:
        if rect_height > 1:
            rect_height -= 1
    if keys[pygame.K_3]:
        v_buffer += 1
    if keys[pygame.K_4]:
        if v_buffer > 1:
            v_buffer -= 1
    if keys[pygame.K_5]:
        h_buffer += 1
    if keys[pygame.K_6]:
        if h_buffer > 1:
            h_buffer -= 1
    if keys[pygame.K_7]:
        if min_width < max_width:
            min_width += 1
    if keys[pygame.K_8]:
        if min_width > 1:
            min_width -= 1
    if keys[pygame.K_9]:
        max_width += 1
    if keys[pygame.K_0]:
        if max_width > 1 and max_width > min_width:
            max_width -= 1
    
    # recalculate things based on key presses
    row_height = rect_height + v_buffer
    row_count = int(YRES/row_height)


    # draw rects
    for row in range(row_count):
        y_pos = (v_buffer/2)+(row*row_height)
        for rect_data in rects[row]:
            rect = pygame.Rect(rect_data[0],y_pos,rect_data[1],rect_height)
            pygame.draw.rect(gameDisplay,WHITE,rect)

    # move rects
    move_rects(rects, speed)

    pygame.display.update()
    fpsClock.tick(FPS)

