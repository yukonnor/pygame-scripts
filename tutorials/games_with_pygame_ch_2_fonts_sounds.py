'''
Chapter 2 Notes & Script from "Making Games with Python and Pygame"
https://inventwithpython.com/pygame/chapter2.html

Fonts, Anti-Aliasing, Sounds
'''
import pygame, sys
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from colors import *         # import the color variables from local file
import time

pygame.init()     

# set up the display window
gameDisplay = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Hellow World!')

# define font stuff
fontObj = pygame.font.Font('freesansbold.ttf', 32)                  # create font object
textSurfaceObj = fontObj.render('Hello world!', True, green, blue)  # create a surface and draw text on it. True turns on ant-aliasing
textRectObj = textSurfaceObj.get_rect()                             # create a rect object from the text surface object that willbe used for placement during blit()
textRectObj.center = (200, 150)                                     # set position of rect obj using its center point

# define sound stuff
soundObj = pygame.mixer.Sound('match1.wav')

# Loading and playing background music:
pygame.mixer.music.load('tetrisb.mid')
pygame.mixer.music.play(-1, 0.0)   # start the backgroud music, loop indefinitely
# pygame.mixer.music.stop()  # stop the backgroud music


# main game loop
while True: 
    gameDisplay.fill(white)     # clear screen (fill with white)  
    gameDisplay.blit(textSurfaceObj, textRectObj)  # blit the text surface obj to the gameDisplay at rect position

    pygame.display.update()

    soundObj.play()
    time.sleep(1)     # wait and let the sound play for 1 second
    soundObj.stop()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

'''
NOTES

Sounds
* First create a pygame.mixer.Sound object by calling the pygame.mixer.Sound() constructor function
  * It takes one string parameter, which is the filename of the sound file. 
  * Pygame can load WAV, MP3, or OGG files. 
* To play a sound object, call the Sound object’s play() method. 
  * The program execution continues immediately after play() is called; it does not wait for the sound to finish playing before moving on to the next line of code.
* If you want to immediately stop the Sound object from playing call the stop() method. 
  * The stop() method has no arguments. 
* Pygame can only load one music file to play in the *background* at a time. 
  * To load a background music file, call the pygame.mixer.music.load() function and pass it a string argument of the sound file to load. 
  * This file can be WAV, MP3, or MIDI format.
  * To begin playing the loaded sound file as the background music, call the pygame.mixer.music.play(-1, 0.0) function. 
    * The -1 argument makes the background music forever loop when it reaches the end of the sound file. 
    * If you set it to an integer 0 or larger, then the music will only loop that number of times instead of looping forever. 
    * The 0.0 means to start playing the sound file from the beginning. If you pass a larger integer or float, the music will begin playing that many seconds into the sound file. 
* To stop playing the background music immediately, call the pygame.mixer.music.stop() function.
'''