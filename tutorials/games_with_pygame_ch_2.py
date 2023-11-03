'''
Chapter 2 Notes & Script from "Making Games with Python and Pygame"
https://inventwithpython.com/pygame/chapter2.html
'''
import pygame, sys
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time

pygame.init()                                      # good practice to init pygame before calling any pygame function
DISPLAYSURF = pygame.display.set_mode((400, 300))  # creates and assigns a pygame surface object (window)
DISPLAYSURF.fill((0,0,0))                          # set fill of surface object to be black
pygame.display.set_caption('Hello World!')         # sets the caption text that will appear at the top of the window

# Game Loop & States
'''
A game loop does three main things:
1.      Handles events.
2.      Updates the game state.
3.      Draws the game state to the screen.
'''
while True: # main game loop
    for event in pygame.event.get():  # checks which events have been created (returns a list of Event objects for each event that has happened since the last time the pygame.event.get() function was called)
        if event.type == QUIT:        # look for "QUIT" event.type. Variable name found in pygame.locals
            pygame.quit()             # quits all pygame functions / code. Should be called first.
            sys.exit()                # Exit from Python

    pygame.display.update()           # draws the Surface object returned by pygame.display.set_mode() to the screen



'''
NOTES

Event Objects
* The list of Event objects returned from pygame.event.get() will be in the order that the events happened.
* Have an attribute called 'type' which tells us what kind of event the object represents. Pygame has a constant variable for each of possible types in the pygame.locals modules.

Surface Objects
* Surface objects are objects that represent a rectangular 2D image.
* The Surface object returned by pygame.display.set_mode() is called the display Surface.
  * Anything that is drawn on the display Surface object will be displayed on the window when the pygame.display.update() is called. 
* Often your program will draw several different things to a Surface object. Once you are done drawing everything on the display Surface object for this iteration of the game loop (called a frame) on a Surface object, it can be drawn to the screen. 
  * The computer can draw frames very quickly, and our programs will often run around 30 frames per second (that is, 30 FPS). 

Colors
* (R, G, B, alpha) - all 0-255
  * no alpha or alpha set to 255 = fully opaque. alpha set to 0 = full transparent (invisible)
* In order to draw using transparent colors, you must create a Surface object with the convert_alpha() method
  * ex: anotherSurface = DISPLAYSURF.convert_alpha()
  * Once things have been drawn on the Surface object stored in anotherSurface, then anotherSurface can be “blitted” (that is, copied) to DISPLAYSURF so it will appear on the screen
* An alternative to defining color using (R,G,B) tuple, you can use a pygame.Color object
  * Create Color objects by calling the pygame.Color() constructor function and passing either three or four integers.
  * ex: myColor = pygame.Color(255, 0, 0, 128)
  * ? Not exactly sure why this is any better...

Rect Objects
* A rectangular area object created by pygame.Rect(X top left, Y top left, width, height). Object is simply a tuple. 
  * spamRect = pygame.Rect(10, 20, 200, 300) --> spamRect == (10, 20, 200, 300) --> True
* A Rect object also calculates the coordinates for other features of the rectangle. 
  * X coordinate of the right edge of the object use the object’s `right` attribute: spamRect.right --> 210
  * You can also reassign value of Rect attributes and all other attributes will be updated: spamRect.right = 350
  * myRect.left | The int value of the X-coordinate of the left side of the rectangle.
  * myRect.right | The int value of the X-coordinate of the right side of the rectangle.
  * myRect.top | The int value of the Y-coordinate of the top side of the rectangle.
  * myRect.bottom | The int value of the Y-coordinate of the bottom side.
  * myRect.centerx | The int value of the X-coordinate of the center of the rectangle.
  * myRect.centery | The int value of the Y-coordinate of the center of the rectangle.
  * myRect.width | The int value of the width of the rectangle.
  * myRect.height | The int value of the height of the rectangle.
  * myRect.size | A tuple of two ints: (width, height)
  * myRect.topleft | A tuple of two ints: (left, top)
  * myRect.topright | A tuple of two ints: (right, top)
  * myRect.bottomleft | A tuple of two ints: (left, bottom)
  * myRect.bottomright | A tuple of two ints: (right, bottom)
  * myRect.midleft | A tuple of two ints: (left, centery)
  * myRect.midright | A tuple of two ints: (right, centery)
  * myRect.midtop | A tuple of two ints: (centerx, top)
  * myRect.midbottom | A tuple of two ints: (centerx, bottom)


'''