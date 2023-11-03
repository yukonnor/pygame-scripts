'''
Chapter 2 Notes & Script from "Making Games with Python and Pygame"
https://inventwithpython.com/pygame/chapter2.html

Primitive Drawing Functions
'''
import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time

pygame.init()     

# set up the display window
DISPLAYSURF = pygame.display.set_mode((500, 400), 0, 32)
pygame.display.set_caption('Drawing')


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

# draw the surface object                                 
DISPLAYSURF.fill(white)
pygame.draw.line(DISPLAYSURF, blue, (100,200), (300,390),5)
pygame.draw.rect(DISPLAYSURF, red, (10,10,250,125))
pygame.draw.circle(DISPLAYSURF, aqua, (150,150), 75)
pygame.draw.polygon(DISPLAYSURF, green, ((490,75), (400,100), (300,390)))
pygame.draw.circle(DISPLAYSURF, olive, (300, 50), 20, 0)        
pygame.draw.ellipse(DISPLAYSURF, maroon, (300, 250, 40, 80), 2)  # just an outline as line width specified (for ellipse: tuple is the bounding rectangle)

# draw individual pixels on surface object
pixArray = pygame.PixelArray(DISPLAYSURF)
pixArray[480][380] = black
pixArray[482][382] = black
pixArray[484][384] = black
pixArray[486][386] = black
pixArray[488][388] = black
del pixArray   # done with drawing individual pixels!

# main game loop
while True: 
    for event in pygame.event.get():  # checks which events have been created (returns a list of Event objects for each event that has happened since the last time the pygame.event.get() function was called)
        if event.type == QUIT:        # look for "QUIT" event.type. Variable name found in pygame.locals
            pygame.quit()             # quits all pygame functions / code. Should be called first.
            sys.exit()                # Exit from Python

    pygame.display.update()           # draws the Surface object returned by pygame.display.set_mode() to the screen



'''
NOTES

Pixel Arrays
* Helps the program run faster (rather than drawing pixels one by one)
* Creating a PixelArray object of a Surface object will “lock” the Surface object. 
  * While a Surface object is locked, the drawing functions can still be called on it, but it cannot have images like PNG or JPG images drawn on it with the blit() method.
* To tell Pygame that you are finished drawing individual pixels, delete the PixelArray object with a del statement. 
  * Deleting the PixelArray object will “unlock” the Surface object so that you can once again draw images on it. 
  * If you forget to delete the PixelArray object, the next time you try to blit (that is, draw) an image to the Surface the program will raise an error that says, “pygame.error: Surfaces must not be locked during blit”.

Display.Update
* Call pygame.display.update() in the loop to make the display Surface update and actually appear on the user’s monitor.
* pygame.display.update() will only make the display Surface (that is, the Surface object that was returned from the call to pygame.display.set_mode()) appear on the screen. 
  * If you want the images on other Surface objects to appear on the screen, you must “blit” them (that is, copy them) to the display Surface object with the blit() method.
'''