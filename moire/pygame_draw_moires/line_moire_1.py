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

HRES = 400
VRES = 400

X_MID = HRES/2
Y_MID = VRES/2


gameDisplay = pygame.display.set_mode((HRES,VRES))
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
    pygame.draw.line(gameDisplay, WHITE, (i*5,0), (i*5,VRES),1)

# draw long lines
def drawLongLine(mouse_x, mouse_y, color, width):
    dx = X_MID - mouse_x
    dy = Y_MID - mouse_y

    #reverse_sign_x = 1 if dx < 0 else -1
    
    if dx == 0:
        slope = 10000000
    else: 
        slope = dy / dx

    # if slope is less than 1, xmin = 0 & xmax = HRES, calculate ymin & ymax
    if 0 < slope < 1:
        xmin = 0
        xmax = HRES
        ymin = -1 * (slope * (xmin - X_MID)) - Y_MID
        ymax = (slope * (X_MID - xmax)) + Y_MID

        pygame.draw.line(gameDisplay,color,(xmin,ymin),(xmax,ymax),width)

    # if slope is greater than or eq to 1, ymin = 0 & ymax = VRES, calculate xmin & xmax

    #x_new = reverse_sign_x * HRES
    #y_new = 0 + slope + (x_new - X_MID)

    

# extrapolate lines


# main game loop
while True:
    gameDisplay.fill(BLACK)     # clear screen 

    # draw background
    for i in range(line_count):
        pygame.draw.line(gameDisplay, WHITE, (i*5,0), (i*5,VRES),2)

    

    # mouse position
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # pygame.draw.line(gameDisplay,green,(HRES/2,VRES/2),(mouse_x,mouse_y),2)
    drawLongLine(mouse_x, mouse_y, GREEN, 2)

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