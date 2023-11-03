
'''
This scetch:

OG_Width = 500px square
1) Set width + height to 500 * 1.5 = 750
2) Set viewbox to (-125, -125, 750, 750)
3) Set rotate to (45deg, 250, 250)

1) To rotate while maintaining the ORIGINAL SIZE, scale up both the viewport (width / height) and the view box by ~1.5. This makes the canvas larger but keeps the original pixel measurements / size
2) Now that the canvas is larger and the shape is the same size, we should center the shape in the new canvas size by offsetting the 
   start points of the viewbox: -(New size - old size)/2
3) Rotate the imgage by setting the center rotation pivot point to old size / 2 


ACTUALLY: The max rotation width (~1.5 og_width) needs to fit within the new viewport width 

'''

import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors import *         # import the color variables from local file
import io                    # to manipulate text properties of SVG images

pygame.init()  

# determin speed of animation
FPS = 15                       
fpsClock = pygame.time.Clock() 

XRES = 800 # w = Fullscreen (move below screen setup if fullscreen)
YRES = 800 # h = Fullscreen

screen = pygame.display.set_mode((XRES,YRES))              #Set display to window
#screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #Set display to full screen
w, h = pygame.display.get_surface().get_size()

XRES = w # w = Fullscreen (move below screen setup if fullscreen)
YRES = h
XMID = XRES/2
YMID = YRES/2

svg_scale = 1

FILEPATH = '/Users/concon/pygame-scripts/moire/'
SVG_NAME = 'my_svg.svg'

# Load and Scale SVG Images to a Pygame Surface:
def load_and_scale_svg(filename, og_svg_width, og_svg_height, scale, angle = None):
    svg_string = open(filename, "rt").read()
    
    # as we're multiplying things by default by 1.5 to support rotation (max length of diagonal), to mainain the original scale (1) we need to multiply by 1.5
    scale = scale * 1.5
    
    # update the width of the viewport to be wide enough to see full image when rotating
    # TODO: THIS WILL NEED TO CHANGE ONCE SCALING
    svg_string = svg_string.replace(f'width="{og_svg_width}"', f'width="{og_svg_width * 1.5 * scale}"')
    svg_string = svg_string.replace(f'height="{og_svg_height}"', f'height="{og_svg_height * 1.5 * scale}"')
    
    # because we're updating the viewport, we need to update the viewbox to maintain the same scale
    viewbox_offset = -1 * (((og_svg_width * 1.5) - og_svg_width)/2)
    svg_string = svg_string.replace(f'viewBox="0 0 {og_svg_width} {og_svg_width}"', f'viewBox="{viewbox_offset} {viewbox_offset} {og_svg_width*1.5} {og_svg_width*1.5}"')
    
    # if an angle is provided, attempt to rotate the svg by that angle
    if angle:      
        # rotate around image's center point
        mid_x = og_svg_width / 2
        mid_y = og_svg_height / 2
        string_input_point = svg_string.find('<g') 
        svg_string = svg_string[:string_input_point+2] + f' transform="rotate({angle}, {mid_x}, {mid_y})"' + svg_string[string_input_point+2:]  # rotate around center 
    
    #print(svg_string)
   
    return pygame.image.load(io.BytesIO(svg_string.encode()))

# Startup Sequence
top_img_og_width = 500
top_img_og_height = 500
top_angle = 0
# Load and scale the svg: 
top_filename = FILEPATH + SVG_NAME
top_img_svg = load_and_scale_svg(top_filename, top_img_og_width, top_img_og_height, svg_scale, top_angle)
top_img_rect = top_img_svg.get_rect()
x = XMID
y = YMID
top_img_rect.center = (x, y) 

# set mouse cursor to be invisible
pygame.mouse.set_visible(False)
mouse_pos_last = [0,0]

# Scale, rotation and position variables for real time scaling during the sketch
dx = 2
dy = 2
change_scale = False
btm_scale = svg_scale
top_scale = svg_scale
top_transformed_img = top_img_svg

# Main Game Loop
while True:
    screen.fill(WHITE)     # clear screen 

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # determine if any arrow key was pressed
            if event.key == pygame.K_SPACE:
                pass
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_UP:
                top_scale += .1
                change_scale = True  # only change the scale when it changes to avoid slowdowns
            if event.key == pygame.K_DOWN:
                top_scale -= .1
                change_scale = True             

     # Checking pressed / holds down keys
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_w]:
        y = top_img_rect.centery - dy
        top_img_rect.centery = y
    if keys[pygame.K_s]:
        y = top_img_rect.centery + dy
        top_img_rect.centery = y
    if keys[pygame.K_a]:
        x = top_img_rect.centerx - dx
        top_img_rect.centerx = x
    if keys[pygame.K_d]:
        x = top_img_rect.centerx + dx
        top_img_rect.centerx = x
    if keys[pygame.K_COMMA]: # < arrow
        top_angle += 0.5
        change_scale = True  # only change the scale when it changes to avoid slowdowns
    if keys[pygame.K_PERIOD]:  # > arrow
        top_angle -= 0.5
        change_scale = True
    
    # Scale and rotate images
    if change_scale:
        print("Scale changing to:", top_scale, "Angle changing to:", top_angle)
        top_transformed_img = load_and_scale_svg(top_filename, top_img_og_width, top_img_og_height, top_scale, top_angle)
        top_img_rect = top_transformed_img.get_rect()
        top_img_rect.center = (x,y) # latest x,y position
        change_scale = False
   
    # Display images
    #screen.blit(btm_transformed_img, btm_img_rect)
    screen.blit(top_transformed_img, top_img_rect)
    pygame.draw.rect(screen, RED, top_img_rect, 5)
        
    pygame.display.update()

    fpsClock.tick(FPS)

