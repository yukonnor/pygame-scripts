'''
CLEAR SCREEN FUNCTIONALITY
'''

import pygame

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,128,0)
blue = (0,0,255)
aqua = (0, 255, 255)
fuchsia = (255, 0, 255)
gray = (128, 128, 128)
lime = (0, 255, 0)
maroon = (128, 0, 0)
navy_blue = (0, 0, 128)
olive = (128, 128, 0)
purple = (128, 0, 128)
silver = (192, 192, 192)
teal = (0, 128, 128)
yellow = (255, 255, 0)

colors = [maroon, red, yellow, green, aqua, teal, blue, navy_blue, purple]

gameDisplay = pygame.display.set_mode((800,600))
gameDisplay.fill(black)

pixArray = pygame.PixelArray(gameDisplay)

pixArray[10][20] = green # set color of specific pixel

ball = pygame.Rect(0,0,10,10)

i = 0

loop_count = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    # CLEAR SCREEN
    gameDisplay.fill((0,0,0))    
    
    # CHANGE COLORS
    if loop_count % 4 == 0:
        if i > len(colors)-2:
            i = 0
        else:
            i += 1

    pygame.draw.circle(gameDisplay,colors[i],ball.center,5)
    ball.move_ip(1,1)
    pygame.display.update()

    loop_count += 1
