import pygame
from pygame.locals import *
import colors # local file with color info
import time

# pygame setup 
pygame.init()  

FPS = 30                       
fpsClock = pygame.time.Clock() 

HRES = 400
VRES = 400

gameDisplay = pygame.display.set_mode((HRES,VRES))
gameDisplay.fill(colors.BLACK)

BG_COLOR = colors.GRAY

UP = 'Up pressed!'
DOWN = 'Down pressed!'
LEFT = 'Left pressed!'
RIGHT = 'Right pressed!'
RED = 'Changed color to red!'
GREEN = 'Changed color to green!'
BLUE = 'Changed color to blue!'

t0 = time.time()

# create font object
font_message = pygame.font.SysFont('helvetica.ttf', 48) # font name, size (size cannot be changed)
font_default = pygame.font.SysFont('helvetica.ttf', 24)
text_color = colors.GREEN  # starting color
default_message = 'Press up, down, left, right OR r,g,b!'
message = ''  
display_message = False    # define display_message

# Get fonts
#fonts = pygame.font.get_fonts()
#print(len(fonts))
#for f in fonts:
#    print(f)


# main game loop
while True:
    
    current_time = time.time()

    gameDisplay.fill(BG_COLOR)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            key_press_time = time.time()
            # determine if a letter key was pressed
            if event.key == pygame.K_r:
                message = RED
                text_color = colors.RED
                display_message = True
            elif event.key == pygame.K_g:
                message = GREEN
                text_color = colors.GREEN
                display_message = True
            elif event.key == pygame.K_b:
                message = BLUE
                text_color = colors.BLUE
                display_message = True
            elif event.key == pygame.K_UP:
                message = UP
                display_message = True
            elif event.key == pygame.K_DOWN:
                message = DOWN
                display_message = True
            elif event.key == pygame.K_LEFT:
                message = LEFT
                display_message = True
            elif event.key == pygame.K_RIGHT:
                message = RIGHT
                display_message = True
                
    
    if display_message:
        #todo
        img = font_message.render(message, True, text_color)  # creates a surface for the message using the predefined font object
        rect = img.get_rect()                                 # Pygame creates a new rect with the size of the image surface and the x, y coordinates (0, 0)
        pygame.draw.rect(img, colors.BLUE, rect, 1)           # draws the rect on the message surface

        gameDisplay.blit(img, (20, 20))               # display the message surface on the main gameDisplay surface at (20,20)

        # hide message after three seconds of no key presses
        if current_time - key_press_time > 3:
            display_message = False
    else:
        default_img = font_default.render(default_message, True, colors.BLACK)

        gameDisplay.blit(default_img, (20, 20))






    

    pygame.display.update()

