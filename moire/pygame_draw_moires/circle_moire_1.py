import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors import *         # import the color variables from local file
from pygame import gfxdraw

pygame.init()  

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

dispayWidth = 400
dispayHeight = 300

gameDisplay = pygame.display.set_mode((dispayWidth,dispayHeight))
gameDisplay.fill(BLACK)


# create circle attributes for 10 circles
circle_count = 10
radius = []
x = []
y = []
direction = []

for i in range(circle_count):
    radius.append(50)
    x.append(50 + (i*10))
    y.append(150)
    direction.append('right')  

print(radius)
print(x)
print(y)
print(direction)

# draw background lines
line_count = 80  # one verticle line every 5 pixels
for i in range(line_count):
    pygame.draw.line(gameDisplay, WHITE, (i*5,0), (i*5,dispayHeight),1)


# main game loop
while True:
    gameDisplay.fill(BLACK)     # clear screen 

    for i in range(line_count):
        pygame.draw.line(gameDisplay, WHITE, (i*5,0), (i*5,dispayHeight),2)

    
    for circle in range(circle_count):
        if direction[circle] == 'right':
            x[circle] += 1
            if x[circle] == dispayWidth - radius[circle]:
                direction[circle] = 'left'
        elif direction[circle] == 'left':
            x[circle] -= 1
            if x[circle] == radius[circle]:
                direction[circle] = 'right'
        
        pygame.gfxdraw.aacircle(gameDisplay, x[circle] ,y[circle], radius[circle], BLACK)
        pygame.gfxdraw.aacircle(gameDisplay, x[circle] ,y[circle], radius[circle]-1, BLACK) # doubling up to make thicker boarder

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()

    fpsClock.tick(FPS)
