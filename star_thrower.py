import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
import colors         # import the color variables from local file
from pygame import gfxdraw
import random

pygame.init()  

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

HRES = 400
VRES = 400

X_MID = HRES/2
Y_MID = VRES/2

gameDisplay = pygame.display.set_mode((HRES,VRES))
gameDisplay.fill(colors.BLACK)

print(pygame.FULLSCREEN)

# create stars (dots)
num_stars = 50
star_x = []      # list of x coords for stars
star_y = []      # list of y coords for stars
speed_x = 3      # initial speed in x direction
speed_y = 2      # initial speed in y direction

# draw center object
def draw_center_object(x, y, r, shadowOffx, shadowOffy):
  # draw circle with shaddow at x,y
  
  # draw shaddow first at an offset 
  pygame.draw.circle(gameDisplay, colors.BLACK, (x + shadowOffx, y + shadowOffy), r) # (surface, color, center, radius, width=0)
  pygame.draw.circle(gameDisplay, colors.WHITE, (x + shadowOffx, y + shadowOffy), r, 2) # (surface, color, center, radius, width=0)

  # draw circle
  pygame.draw.circle(gameDisplay, colors.BLACK, (x, y), r)
  pygame.draw.circle(gameDisplay, colors.WHITE, (x, y), r, 2)

def init_star_positions():
    # create the initial positions for the stars
    for star in range(num_stars):
        star_x.append(random.randint(0,HRES))
        star_y.append(random.randint(0,VRES))

def move_stars():
    # move all stars in a certain direction (based on midi inputs: x,y,speed)
    for star in range(num_stars):
        star_x[star] += speed_x
        star_y[star] += speed_y

    # if star moves off screen, regenerate at random position
    # TODO: redraw at random location opposite of direction
    for star in range(num_stars):
        if star_x[star] > HRES:
            star_x[star] = 0
            star_y[star] = random.randint(0,VRES)
        elif star_x[star] < 0:
            star_x[star] = HRES
            star_y[star] = random.randint(0,VRES)
        elif star_y[star] > VRES: 
            star_x[star] = random.randint(0,VRES)
            star_y[star] = 0
        elif star_y[star] < 0:
            star_x[star] = random.randint(0,VRES)
            star_y[star] = VRES

def draw_stars(num_stars, star_x,star_y):
    # draw the stars

    for star in range(num_stars):
        x = star_x[star]
        y = star_y[star]
        pygame.draw.rect(gameDisplay, colors.WHITE, (x,y,5,5)) # draw 'line' with same start and end point


# draw background lines
line_count = 80  # one verticle line every 5 pixels
for i in range(line_count):
    pygame.draw.line(gameDisplay, colors.WHITE, (i*5,0), (i*5,VRES),1)

# set star positions
init_star_positions()

print(star_x)

# main game loop
while True:
    gameDisplay.fill(colors.BLACK)     # clear screen 

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

    # draw background
    #for i in range(line_count):
    #    pygame.draw.line(gameDisplay, colors.colors.WHITE, (i*5,0), (i*5,VRES),2)

    # move stars
    move_stars()

    # draw stars
    draw_stars(num_stars, star_x, star_y)

    # draw center object over stars
    draw_center_object(X_MID,Y_MID,50,10,10)

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()

    fpsClock.tick(FPS)


'''
NOTES:

- It's possible to draw lines with points outside the game display boundary

'''