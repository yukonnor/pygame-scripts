import pygame
from time import sleep
import random

XRES = 800
YRES = 600
MIDPOINT_X = XRES / 2
WHITE = (255,255,255)
BLACK = (0,0,0)

screen = pygame.display.set_mode((XRES,YRES))
screen.fill(BLACK)
clock = pygame.time.Clock()

# Import image
arm = pygame.image.load('cowboy_milkyway/arm-right.png')
arm_rect = arm.get_rect()  
print(arm_rect)
scale = 0.3                                         # scale the image down by this amount
scaled_arm = pygame.transform.rotozoom(arm,0,scale) # scale image down
arm_rect = scaled_arm.get_rect()                    # get new size of the image to determine offset amnts
print(arm_rect)


# Based on this specific imaage to rotate image around the 'shoulder', x offset needs to be 
# roughly 20% of the width of the original image position, and halfway down
offset_x =  int(arm_rect.width * .2)
offset_y =  int(arm_rect.height * .5)

# Rotation variables:
# Define the x,y pivot point for the rotation
pivot = [XRES/2, YRES/2]              
# A vector is an object that has both a magnitude and a direction. 
# In pygame it seems to mean the 'destination' coordinates from an origin of 0,0
# This offset vector will be added to the pivot point, so the
# resulting rect will be blitted at `rect.topleft + offset`.
offset = pygame.math.Vector2(offset_x, offset_y)   # move image x,y from the pivot point
angle = 0
 
    
# Rotate an image around a pivot point   
def rotate(surface, angle, pivot, offset):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
        offset (pygame.math.Vector2): This vector is added to the pivot.
    """
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image, final arg is "scale"
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot+rotated_offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

while True:

    screen.fill(BLACK)           # fully clear screen    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_UP:
                angle += 5
            if event.key == pygame.K_DOWN:
                angle += -5
            if event.key == pygame.K_p:
                print(rect)
                print(f'Rect width: {rect.width}. Rect height: {rect.height}')
                
    
    # rotate image around its center point
    # 1. Rotate the image
    # 2. Get a new rect with the center of the original rect
    # 3. Blit position is top left corner of the image
    
    rotated_image,rect = rotate(scaled_arm, angle, pivot, offset)
    screen.blit(rotated_image,rect)
    pygame.draw.circle(screen, WHITE, (pivot[0],pivot[1]), 10)  # draw the pivot point
    pygame.draw.rect(screen,WHITE,rect,2)
    
    pygame.display.set_caption('Angle: {}'.format(angle))
    
    pygame.display.flip()
    clock.tick(30)
    

    
    
    # rotate image around pre-defined pivot point