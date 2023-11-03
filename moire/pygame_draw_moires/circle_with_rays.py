'''
TODO:
- changes shape
- decrease shape size
- make into a game 

'''

import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
import moire_colors         # import the color variables from local file
from pygame import gfxdraw
import random

pygame.init()  

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

#gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
w, h = pygame.display.get_surface().get_size()
XRES = w
YRES = h

X_MID = XRES/2
Y_MID = YRES/2

gameDisplay.fill(moire_colors.BLACK)

print(pygame.FULLSCREEN)

# create variables
show_center_shape = True
radius = XRES/10   # starting radius size
line_spacing = 10 # space between each line 
line_width = 1
assert XRES % line_spacing == 0, "Line spacing needs to fit within XRES"
assert YRES % line_spacing == 0, "Line spacing needs to fit within YRES"
line_origin_x = []
line_origin_y = []
center_point = [X_MID, Y_MID]   


speed_x = 3      # initial speed in x direction
speed_y = 2      # initial speed in y direction

# draw center object
def draw_center_circle(x, y, r):
  # draw a solid circle with outline at x,y
  pygame.draw.circle(gameDisplay, moire_colors.BLACK, (x, y), r)
  pygame.draw.circle(gameDisplay, moire_colors.WHITE, (x, y), r, 2)

def init_lines():
    # create the initial positions for the lines
    
    count_top_lines = int(XRES/line_spacing) - 1    # no corners
    count_side_lines = int(YRES/line_spacing)       # top corners
    count_bottom_lines = int(XRES/line_spacing) + 1 # both bottom corners

    # top of screen
    for line in range(count_top_lines):
        line_origin_x.append((line*line_spacing)+line_spacing)  # fill middle lines (top corners done on sides)
        line_origin_y.append(0)
    
    # left of screen
    for line in range(count_side_lines):
        line_origin_x.append(0)  
        line_origin_y.append(line*line_spacing)
    
    # right of screen
    for line in range(count_side_lines):
        line_origin_x.append(XRES)  
        line_origin_y.append(line*line_spacing)

    # bottom of screen
    for line in range(count_bottom_lines):
        line_origin_x.append(line*line_spacing)  
        line_origin_y.append(YRES)

def draw_lines(line_origin_x, line_origin_y, center_point, line_width):
    for i,val in enumerate(line_origin_x):
        pygame.draw.line(gameDisplay, moire_colors.WHITE, [line_origin_x[i],line_origin_y[i]], center_point, line_width)



# set line coords 
init_lines()

# main game loop
while True:
    gameDisplay.fill(moire_colors.BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # determine if any arrow key was pressed
            if event.key == pygame.K_SPACE:
                center_point = [X_MID, Y_MID]  # reset to center point
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    keys = pygame.key.get_pressed()  #checking pressed keys
    if keys[pygame.K_UP]:
        center_point[1] -= 5
    if keys[pygame.K_DOWN]:
        center_point[1] += 5
    if keys[pygame.K_LEFT]:
        center_point[0] -= 10
    if keys[pygame.K_RIGHT]:
        center_point[0] += 10
    # increase radius if r pressed, decrease if shift + r pressed    
    if keys[pygame.K_r]:
        radius += 4
    if keys[pygame.K_r] and keys[pygame.K_LSHIFT]:
        radius -= 4
    


    # draw stars
    draw_lines(line_origin_x, line_origin_y, center_point, line_width)

    # draw center object over stars
    if show_center_shape:
        draw_center_circle(center_point[0],center_point[1],radius)


    pygame.display.update()

    fpsClock.tick(FPS)


'''
NOTES:

- It's possible to draw lines with points outside the game display boundary

'''