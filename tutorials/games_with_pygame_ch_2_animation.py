'''
Chapter 2 Notes & Script from "Making Games with Python and Pygame"
https://inventwithpython.com/pygame/chapter2.html

Animations
'''
import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from colors import *         # import the color variables from local file

pygame.init()     

FPS = 30                       # define frames per second
fpsClock = pygame.time.Clock() # this object can help us make sure our program runs at a certain maximum FPS

# set up the display window
gameDisplay = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('Animation')

# get the cat image
catImg = pygame.image.load('catlogo.png')   # must be in same file / directory as script! Returns a surface object with the image on it!
catx = 10
caty = 10
direction = 'right'

# main game loop
while True: 
    gameDisplay.fill(white)     # clear screen (fill with white)   
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'
    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'
    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'

    gameDisplay.blit(catImg, (catx, caty)) # copy catImg surface to main gameDisplay surface at location x,y (topleft corner of img)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

'''
NOTES

Clock Object
* This Clock object will ensure that our game programs don’t run too fast by putting in small pauses on each iteration of the game loop. 
  * If we didn’t have these pauses, our game program would run as fast as the computer could run it. This is often too fast for the player, and as computers get faster they would run the game faster too. 
  * A call to the tick() method of a Clock object in the game loop can make sure the game runs at the same speed no matter how fast of a computer it runs on.
  * The tick() method should be called at the very end of the game loop, after the call to pygame.display.update(). 
  * The length of the pause is calculated based on how long it has been since the previous call to tick()
* Setting the FPS provided to the tick() menthod to a lower value would make the program run slower. Setting it to a higher value would make the program run faster.

Images & Blitting
* Images are also called "sprites"
* Pygame is able to load images onto Surface objects from PNG, JPG, GIF (won't animate), and BMP image files.
* The pygame.image.load() function call will return a *Surface object* that has the image drawn on it. 
  * This Surface object will be a separate Surface object from the display Surface object, so we must blit (that is, copy) the image’s Surface object to the display Surface object. 
* Blitting is drawing the contents of one Surface onto another. It is done with the blit() Surface object method.
  * blit(source, dest, area=None, special_flags=0)
  * You cannot blit to a Surface that is currently “locked”
  * The dest argument can either be a pair of coordinates representing the position of the upper left corner of the blit or a Rect, where the upper left corner of the rectangle will be used as the position for the blit. 
  * The size of the destination rectangle does not effect the blit.
  * An optional area rectangle can be passed as well. This represents a smaller portion of the source Surface to draw.
'''