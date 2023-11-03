'''
TODO:
- Resize original images to be roughly appropriate scales 

'''

import pygame
from time import sleep
import random

XRES = 800
YRES = 600
MIDPOINT_X = XRES / 2
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

screen = pygame.display.set_mode((XRES,YRES))
screen.fill((0,0,0))

# Set up a transparent surface

night_sky = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/night_sky.png')
scaled_night_sky = pygame.transform.scale(night_sky, (XRES,YRES))
opacity = 100 # 0-255 0(transparent) - 255 (opaque)
scaled_night_sky.set_alpha(opacity)  
transparent_surface = pygame.Surface((XRES,YRES), pygame.SRCALPHA, 32)
transparent_surface.fill((0,0,0,opacity))
transparent_surface = transparent_surface.convert_alpha()

# Import images
images = ['hat', 'face', 'shirt', 'arms']

hat = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/cowboy-hat-2.png') 
hat_orig_size = [600, 336] 
hat_size = [200, 112]            # orignal / default scaled size for hat
hat_pivot = [XRES/2 , YRES/5]    # pivot point at the center of the hat
hat_angle = 0                    # neg CCW (based on rotate function)
hat_dir = [1,1]
hat_speed = [3,5]
hat_size_dir = [1,1]
hat_growth_speed = [5,5]

face = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/mannequin-head.png')
face_rect_orig = face.get_rect()
face_pivot = [0, 0]  
face_angle = 0   # neg CCW (based on rotate function)
face_angle_min_max = [-15, 15]
face_angle_dir = 1

shirt = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/shirt.png')
shirt_rect_orig = shirt.get_rect()
shirt_pivot = [0, 0]  
shirt_angle = 0   # neg CCW (based on rotate function)
shirt_angle_min_max = [-6, 6]
shirt_angle_dir = -1

arm_left = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/arm-left-copy.png')
arm_left_pivot = [0, 0]  
arm_right_pivot = [0, 0]  
arm_right_angle = 15   # pos, CW | neg CCW (based on rotate function)
arm_left_angle = -1 * arm_right_angle   
arm_angle_min_max = [5, 40]
arm_right_angle_dir = 1

cloud = pygame.image.load('/Users/concon/pygame-scripts/cowboy_milkyway/night_sky_cloud.png')
cloud_rect_orig = cloud.get_rect()
cloud_scale = 1

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

def update_image_positions(hat_pivot, hat_scale):
    # all all image pivot points are (currently) based off the hat pivot point, they can all
    # be updated when the hat's pivot point is updated
    
    face_scale = hat_scale * 0.8
    face_pivot[0] = hat_pivot[0]
    face_pivot[1] = hat_pivot[1] + (face_rect_orig.height * face_scale * .5)
    
    shirt_scale = hat_scale * .8 
    shirt_pivot[0] = hat_pivot[0]       
    shirt_pivot[1] = face_pivot[1] + (shirt_rect_orig.height * shirt_scale * .6)
    
    arm_left_pivot[0] = shirt_pivot[0] - (shirt_rect_orig.height * shirt_scale * .25)     # around left shoulder
    arm_left_pivot[1] = shirt_pivot[1] - (shirt_rect_orig.height * shirt_scale * .2)
    arm_right_pivot[0] = shirt_pivot[0] + (shirt_rect_orig.height * shirt_scale * .25)    # around right shoulder
    arm_right_pivot[1] = shirt_pivot[1] - (shirt_rect_orig.height * shirt_scale * .2)
    
    

def animate_hat_size():
    # Animate size of hat
    if (hat_size[0] >= 400):
        hat_size_dir[0] = -1
    if (hat_size[0] <= 100):
        hat_size_dir[0] = 1
    if (hat_size[1] >= hat_size[0] * .5):
        hat_size_dir[1] = -1
    if (hat_size[1]) <= hat_size[0] * .3:
        hat_size_dir[1] = 1
        
    # Adjust size (and thus scale) of the cowboy hat)    
    hat_size[0] += hat_size_dir[0] * hat_growth_speed[0]
    hat_size[1] += hat_size_dir[1] * hat_growth_speed[1]
    
    return hat_size

def animate_hat_position():
    # Animate position of hat in X direction
    if (hat_pivot[0] >= XRES/2 + XRES/4):
        hat_dir[0] = -1
    if (hat_pivot[0] <= XRES/2 - XRES/4):
        hat_dir[0] = 1
    # Animate position of hat in Y direction
    if (hat_pivot[1] >= YRES/2):
        hat_dir[1] = -1
    if (hat_pivot[1] <= 0):
        hat_dir[1] = 1
        
    hat_pivot[0] += hat_dir[0] * hat_speed[0]                  # center the hat horizonally (pivot point is in center of hat)
    hat_pivot[1] += hat_dir[1] * hat_speed[1] # bounce the hat vertically
    
    return hat_pivot

def scale_image(img, new_size, orig_size):
    # Some of the transforms are destructiv (resizing and rotating). It is better to 
    # re-transform the original surface than to keep transforming an image multiple times.
    scaled_img = pygame.transform.scale(img, new_size)
    scaled_img_rect = scaled_img.get_rect()
    
    # Get rough scale of the transformation to scale the other elements of the cowboy:
    x_scale = scaled_img_rect.width / orig_size[0]
    y_scale = scaled_img_rect.height / orig_size[1]
    
    return scaled_img, x_scale

def scale_zoom_image(img, scale):
    scaled_img = pygame.transform.rotozoom(img, 0, scale)
    
    return scaled_img

def set_pivot_offset(x,y):
    img_pivot_offset = pygame.math.Vector2(x, y) 
    
    return img_pivot_offset

def update_angle(current_angle, direction, amt, min_max):
    print("At beginning of function:", direction)
    if current_angle > min_max[1]:
        print("Current Angle:", current_angle, "Max:", min_max[1], "Change direction to -1")
        direction = -1
    elif current_angle < min_max[0]:
        print("Current Angle:", current_angle, "Min:", min_max[0], "Change direction to +1")
        direction = 1
    else: 
        print("Current Angle:", current_angle, "Dir:", direction, "Keep direction")
        
    new_angle = current_angle + (amt * direction)   
    return new_angle, direction

def drunk_angle(current_angle, amt, min_max):
    # drunk random between an images min and max angles
    dir = random.choice([-1, 1])
    
    if current_angle > min_max[1]:
        dir = -1
    elif current_angle < min_max[0]:
        dir = 1
        
    new_angle = current_angle + (amt * dir)   
    return new_angle

    
animate = True
twist_imgs = True
draw_rects = False

while True:

    screen.blit(scaled_night_sky, (0,0))      # clear screen with night sky background (transparent)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_LEFT:
                hat_size[0] += -5
            if event.key == pygame.K_RIGHT:
                hat_size[0] += 5
            if event.key == pygame.K_UP:
                #hat_size[1] += 5
                shirt_angle += 5
                print(shirt_angle)
            if event.key == pygame.K_DOWN:
                # hat_size[1] += -5
                shirt_angle += -5
                print(shirt_angle)
            if event.key == pygame.K_a:
                animate = not animate # turn animate on or off
            if event.key == pygame.K_p:
                pass
            if event.key == pygame.K_r:
                draw_rects = not draw_rects
                
    if animate: 
        hat_size = animate_hat_size()
        hat_pivot = animate_hat_position()
        
    if twist_imgs:
        for img in images:
            if img == 'face':
                if face_angle > face_angle_min_max[1]:
                    face_angle_dir = -1
                elif face_angle < face_angle_min_max[0]:
                    face_angle_dir = 1
                face_angle = face_angle + (1 * face_angle_dir)   
            if img == 'shirt':
                if shirt_angle > shirt_angle_min_max[1]:
                    shirt_angle_dir = -1
                elif shirt_angle < shirt_angle_min_max[0]:
                    shirt_angle_dir = 1
                shirt_angle = shirt_angle + (1 * shirt_angle_dir)  
            if img == 'arms':
                if arm_right_angle > arm_angle_min_max[1]:
                     arm_right_angle_dir = -1
                elif arm_right_angle < arm_angle_min_max[0]:
                    arm_right_angle_dir = 1
                arm_right_angle = arm_right_angle + (1 * arm_right_angle_dir)  
                arm_left_angle = -1 * arm_right_angle
        
            
    # Make Hat Adjustments
    scaled_hat, hat_scale = scale_image(hat, hat_size, hat_orig_size)
    hat_pivot_offset = set_pivot_offset(0,0)
    
    # as all other elements are tied to the hat's position, they can be updated here as well:
    update_image_positions(hat_pivot, hat_scale)
    
    # Make Face Adjuments
    face_scale = hat_scale * 0.8  
    scaled_face = scale_zoom_image(face, face_scale)
    face_pivot_offset = set_pivot_offset(0,0)

    # Make Shirt Adjustments
    shirt_scale = hat_scale * .8 
    scaled_shirt = scale_zoom_image(shirt, shirt_scale) 
    shirt_pivot_offset = set_pivot_offset(0,0)
    
    # Make Left Arm Adjustments
    arm_left_scale = hat_scale * .24
    scaled_arm_left = scale_zoom_image(arm_left, arm_left_scale) 
    scaled_arm_left_rect = scaled_arm_left.get_rect()
    arm_left_offset_x = -1 * scaled_arm_left_rect.width * .5                
    arm_left_offset_y = scaled_arm_left_rect.height * .3   
    arm_left_pivot_offset = set_pivot_offset(arm_left_offset_x, arm_left_offset_y)
    
    # Make Right Arm Adjustments
    scaled_arm_right = pygame.transform.flip(scaled_arm_left, True, False) # imag, flip_x, flip_y
    scaled_arm_right_rect = scaled_arm_right.get_rect()
    arm_right_offset_x = arm_left_offset_x * -1               
    arm_right_offset_y = arm_left_offset_y
    arm_right_pivot_offset = set_pivot_offset(arm_right_offset_x, arm_right_offset_y)
    
    # Make Cloud Adjustments
    cloud_scale = hat_scale * 1.3
    scaled_cloud = scale_zoom_image(cloud, cloud_scale)
    scaled_cloud_rect = scaled_cloud.get_rect()
    cloud_center_x = shirt_pivot[0]
    cloud_center_y = int(shirt_pivot[1] + (shirt_rect_orig.height * shirt_scale) * .6)
    scaled_cloud_rect.center = (cloud_center_x, cloud_center_y) 
        
    ##########################
    # Rotate Images
    rotated_arm_left,rotated_arm_left_rect = rotate(scaled_arm_left, arm_left_angle, arm_left_pivot, arm_left_pivot_offset)
    rotated_arm_right,rotated_arm_right_rect = rotate(scaled_arm_right, arm_right_angle, arm_right_pivot, arm_right_pivot_offset)
    rotated_shirt,rotated_shirt_rect = rotate(scaled_shirt, shirt_angle, shirt_pivot, shirt_pivot_offset)
    rotated_face,rotated_face_rect = rotate(scaled_face, face_angle, face_pivot, face_pivot_offset)
    rotated_hat,rotated_hat_rect = rotate(scaled_hat, hat_angle, hat_pivot, hat_pivot_offset)


    ##########################
    # draw arms
    screen.blit(rotated_arm_left,rotated_arm_left_rect)
    screen.blit(rotated_arm_right,rotated_arm_right_rect)
    # draw shirt
    screen.blit(rotated_shirt,rotated_shirt_rect)
    # draw cloud
    screen.blit(scaled_cloud, scaled_cloud_rect)
    # draw face
    screen.blit(rotated_face,rotated_face_rect)
    # draw cowboy hat
    screen.blit(rotated_hat,rotated_hat_rect)

    
    if False: 
        # draw the pivot points
        pygame.draw.circle(screen, RED, (hat_pivot[0],hat_pivot[1]), 10)  
        pygame.draw.circle(screen, WHITE, (face_pivot[0],face_pivot[1]), 10) 
        pygame.draw.circle(screen, RED, (shirt_pivot[0],shirt_pivot[1]), 10)   
        pygame.draw.circle(screen, GREEN, (arm_left_pivot[0],arm_left_pivot[1]), 10)  
        pygame.draw.circle(screen, BLUE, (arm_right_pivot[0],arm_right_pivot[1]), 10) 
        
        # draw the "circle ship"
        circle_center = [shirt_pivot[0], shirt_pivot[1] + shirt_rect_orig.height * shirt_scale * .8]
        full_diameter = shirt_rect_orig.width * shirt_scale 
        pygame.draw.circle(screen, BLACK, circle_center, full_diameter/2)
        pygame.draw.circle(screen, WHITE, circle_center, full_diameter/2, 1)
        pygame.draw.circle(screen, BLUE, circle_center, full_diameter/3, 1)
        pygame.draw.circle(screen, GREEN, circle_center, full_diameter/4, 1)
        pygame.draw.circle(screen, BLUE, circle_center, full_diameter/5, 1) 



    sleep(.05)
    pygame.display.update()
