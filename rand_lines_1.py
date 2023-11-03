import pygame
from pygame.constants import WINDOWHITTEST
import colors
from time import sleep
import random

XRES = 800
YRES = 600
MIDPOINT_X = XRES / 2
MIDPOINT_Y = YRES / 2

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.BLACK)

num_lines = 50
line = []

def init_lines():
    # start all (x,y) coords for lines at midpoint
    for i in range(num_lines):
        line.append([[MIDPOINT_X,MIDPOINT_Y],[MIDPOINT_X,MIDPOINT_Y]]) # [(x0,y0), (x1, y1)]

init_lines()

while True:

    gameDisplay.fill(colors.BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                pass

    
    for i in range(num_lines):
        line[i][0][0] += random.randint(-2,2)
        line[i][0][1] += random.randint(-2,2) 
        line[i][1][0] += random.randint(-2,2) 
        line[i][1][1] += random.randint(-2,2)              

    # if outside border, redraw at center
    for i in range(num_lines):
        if line[i][0][0] > XRES or line[i][0][0] < 0:
            line[i][0][0] = MIDPOINT_X 
        if line[i][0][1] > YRES or line[i][0][1] < 0:
            line[i][0][1] = MIDPOINT_Y 
        if line[i][1][0] > XRES or line[i][1][0] < 0:
            line[i][1][0] = MIDPOINT_X 
        if line[i][1][1] > YRES or line[i][1][1] < 0:
            line[i][1][1] = MIDPOINT_Y 


    for i in range(num_lines):
        pygame.draw.line(gameDisplay, colors.WHITE, line[i][0], line[i][1], 2)
    

    pygame.display.update()
    
