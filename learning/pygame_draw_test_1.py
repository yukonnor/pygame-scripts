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



gameDisplay = pygame.display.set_mode((800,600))
gameDisplay.fill(black)

pixArray = pygame.PixelArray(gameDisplay)

pixArray[10][20] = green # set color of specific pixel
pixArray.close()

pygame.draw.line(gameDisplay, blue, (100,200), (300,450),5)
pygame.draw.rect(gameDisplay, red, (400,400,250,125))
pygame.draw.circle(gameDisplay, white, (150,150), 75)
pygame.draw.polygon(gameDisplay, green, ((750,75), (400,100), (300,600)))



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    pygame.display.update()
