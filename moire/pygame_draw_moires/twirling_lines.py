import math
import pygame
from pygame.locals import *
import moire_colors  
import random
import time

pygame.init() 

XRES = 400
YRES = 400

gameDisplay = pygame.display.set_mode((XRES,YRES))


# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 


# variables
num_lines = 120
line_len = 100   # half of the line's actual length
draw_area_x_min = 0 - line_len
draw_area_x_max = XRES + line_len
draw_area_y_min = 0 - line_len
draw_area_y_max = YRES + line_len

speed_x = 0
speed_y = 0

line_origin = []
angle = 0
angle_step = 1

adjust_color = 0
red = 0
green = 0
blue = 0

# create origin points for lines
for i in range(num_lines):
    x = random.randint(draw_area_x_min, draw_area_x_max)
    y = random.randint(draw_area_y_min, draw_area_y_max)
    line_origin.append([x,y])  # append set of tuples for each origin point


def move_lines():
    # move all lines in a certain direction (based on inputs: x,y,speed)
    for line in range(num_lines):
        line_origin[line][0] += speed_x
        line_origin[line][1] += speed_y

    # if line moves off screen, regenerate at random position on opposide side of screen
    for line in range(num_lines):
        if line_origin[line][0] > draw_area_x_max:
            line_origin[line][0] = draw_area_x_min
            line_origin[line][1] = random.randint(draw_area_y_min, draw_area_y_max)
        elif line_origin[line][0] < draw_area_x_min:
            line_origin[line][0] = draw_area_x_max
            line_origin[line][1] = random.randint(draw_area_y_min, draw_area_y_max)
        elif line_origin[line][1] > draw_area_y_max: 
            line_origin[line][0] = random.randint(draw_area_x_min, draw_area_x_max)
            line_origin[line][1] = draw_area_y_min
        elif line_origin[line][1] < draw_area_y_min:
            line_origin[line][0] = random.randint(draw_area_x_min, draw_area_x_max)
            line_origin[line][1] = draw_area_y_max

    

loop_count = 0

# ////  MAIN GAME LOOP ////
while True:
    gameDisplay.fill(moire_colors.BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # determine if any arrow key was pressed
            if event.key == pygame.K_UP:
                speed_y -= 1  # negative y in up direction
            elif event.key == pygame.K_DOWN:
                speed_y += 1   # positive y in down direction
            elif event.key == pygame.K_LEFT:
                speed_x -= 1
            elif event.key == pygame.K_RIGHT:
                speed_x += 1
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # calcualate new line orgins based on speed_x and speed_y
    move_lines()
    
    # calculate line points
    for i in range(num_lines):
        x0 = line_origin[i][0] + math.cos(math.radians(angle)) * line_len
        y0 = line_origin[i][1] + math.sin(math.radians(angle)) * line_len
        x1 = line_origin[i][0] - math.cos(math.radians(angle)) * line_len
        y1 = line_origin[i][1] - math.sin(math.radians(angle)) * line_len     
        

        # then render the line 
        if adjust_color:
            pygame.draw.line(gameDisplay, (red,green,blue), (x0,y0), (x1,y1), 1)
        else:
            pygame.draw.line(gameDisplay, moire_colors.WHITE, (x0,y0), (x1,y1), 1)
        

    # adjust the angle
    angle += angle_step
    
    # adjust the color of the lines based on angle
    if adjust_color: 
        color_step = int(255 / 90) 
        # for 90 steps increase colors, for 90 steps decrease colors
        if loop_count <=90:
            red += color_step
            green += color_step
            blue += color_step
        elif loop_count <= 180:
            red -= color_step
            green -= color_step
            blue -= color_step
            if loop_count == 180:
                loop_count = 0

    #print(loop_count, angle, red, green, blue)
    pygame.display.update()

    #time.sleep(.5)

    fpsClock.tick(FPS)
    loop_count += 1