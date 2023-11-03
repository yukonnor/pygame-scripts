import math
import pygame
from pygame.locals import *
import colors  


pygame.init() 

XRES = 400
YRES = 400

gameDisplay = pygame.display.set_mode((XRES,YRES))


# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 



radar_origin = (100,100)
radar_len = 50
angle = 0

# main game loop
while True:
    gameDisplay.fill(colors.GREEN)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    x = radar_origin[0] + math.cos(math.radians(angle)) * radar_len
    y = radar_origin[1] + math.sin(math.radians(angle)) * radar_len

    x0 = 200 + math.cos(math.radians(angle)) * radar_len
    y0 = 200 + math.sin(math.radians(angle)) * radar_len
    x1 = 200 - math.cos(math.radians(angle)) * radar_len
    y1 = 200 - math.sin(math.radians(angle)) * radar_len

    # then render the line radar->(x,y)
    pygame.draw.line(gameDisplay, colors.WHITE, radar_origin, (x,y), 1)
    pygame.draw.line(gameDisplay, colors.WHITE, (x0,y0), (x1,y1), 1)
    
    angle += 1

    pygame.display.update()

    fpsClock.tick(FPS)