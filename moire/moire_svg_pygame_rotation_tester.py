
'''
This scetch:
- Import svg and then rotate using pygame's tools to rotate and scale

IMPORTANT: The frame rate got MUCH BETTER when the image was scaled down.
- AS it takes longer to rotate something larger, you should:
  - Only upscale the size of the BOTTOM image, which will not rotate
  - Only rotate the top image, which will stay at a manageable size (you can scale, but keep adjustments smaller)
  
- You could try to pre-crop all images you are using as round. This will minimize the data in them and will make the rotation edges better?

'''

import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors import *         # import the color variables from local file
import io                    # to manipulate text properties of SVG images

pygame.init()  

# determin speed of animation
FPS = 30                       
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

dx = 2
dy = 2

FILEPATH = '/Users/concon/pygame-scripts/moire/'
SVG_NAMES = ['Cirlces.svg', 'Lines.svg', 'Radial Circle.svg', 'dot_matrix_3.svg']

# Load and Scale SVG Images to a Pygame Surface:
# NOTE: Removing rotation from function in this script as rotating with rotozoom. Becuase no rotation we can remove viewport buffer.
def load_and_scale_svg(svg_string, og_svg_width, og_svg_height, scale, color = None):        
    
    # update the width of the viewport to be wide enough to see full image when rotating
    svg_string = svg_string.replace(f'width="{og_svg_width}"', f'width="{og_svg_width * scale}"', 1)
    svg_string = svg_string.replace(f'height="{og_svg_height}"', f'height="{og_svg_height * scale}"', 1)
    
    # because we're updating the viewport, we need to update the viewbox to maintain the same scale
    svg_string = svg_string.replace(f'viewBox="0 0 {og_svg_width} {og_svg_width}"', f'viewBox="0 0 {og_svg_width} {og_svg_width}"', 1)
    
    # Replace black with color provided
    svg_string = svg_string.replace('black', f'{color}')
   
    return pygame.image.load(io.BytesIO(svg_string.encode())).convert_alpha()

def display_fps():
    font = pygame.font.SysFont("Arial", 24)
    fps_string = "FPS = " + str(int(fpsClock.get_fps()))
    text_to_show = font.render(fps_string, 0, WHITE)
    pygame.draw.rect(screen, BLACK, (0,0,130,40))
    screen.blit(text_to_show, (5,5))

# Startup Sequence
btm_filepath = FILEPATH + SVG_NAMES[3]
btm_svg_string = open(btm_filepath, "rt").read()  # original SVG
btm_img_og_width = 1000
btm_img_og_height = 1000
btm_color = 'blue'

btm_img_svg = load_and_scale_svg(btm_svg_string, btm_img_og_width, btm_img_og_height, svg_scale, btm_color)
btm_img_rect = btm_img_svg.get_rect() # this doesn't appear to ingest the scaleed size, so have to adjust
btm_img_rect.center = (XMID, YMID)  # center the img on the screen

top_filename = FILEPATH + SVG_NAMES[3]
top_svg_string = open(top_filename, "rt").read()  # original SVG
top_img_og_width = 1000
top_img_og_height = 1000
top_color = 'blue'
top_angle = 0

top_img_svg = load_and_scale_svg(top_svg_string, top_img_og_width, top_img_og_height, svg_scale, top_color)
top_img_rect = top_img_svg.get_rect()
x = XMID
y = YMID
top_img_rect.center = (x, y) 

# set mouse cursor to be invisible
pygame.mouse.set_visible(False)
mouse_pos_last = [0,0]

# Scale variables for real time scaling during the sketch
change_btm_scale = False
change_top_scale = False
btm_scale = svg_scale
top_scale = svg_scale
btm_transformed_img = btm_img_svg
top_transformed_img = top_img_svg

show_FPS = True

# Main Game Loop
while True:
    screen.fill(BLACK)     # clear screen 

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            # determine if any arrow key was pressed
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_f:
                show_FPS = not show_FPS
            if event.key == pygame.K_MINUS:
                top_scale -= .1
                change_top_scale = True  
            if event.key == pygame.K_EQUALS: # ie the +PLUS key
                top_scale += .1
                change_top_scale = True 
            if event.key == pygame.K_LEFTBRACKET:
                btm_scale -= .1
                change_btm_scale = True 
            if event.key == pygame.K_RIGHTBRACKET:
                btm_scale += .1
                change_btm_scale = True          

     # Checking pressed / holds down keys
    keys = pygame.key.get_pressed()       
    # BOTTOM IMAGE POSITION:
    if keys[pygame.K_w]:
        btm_img_rect.centery -= dy 
    if keys[pygame.K_s]:
        btm_img_rect.centery += dy 
    if keys[pygame.K_a]:
        btm_img_rect.centerx -= dx 
    if keys[pygame.K_d]:
        btm_img_rect.centerx += dx 
        
    # TOP IMAGE POSITION:
    if keys[pygame.K_UP]:
        x = top_img_rect.centerx - dx
        top_img_rect.centerx = x
    if keys[pygame.K_DOWN]:
        y = top_img_rect.centery + dy
        top_img_rect.centery = y
    if keys[pygame.K_LEFT]:
        x = top_img_rect.centerx - dx
        top_img_rect.centerx = x
    if keys[pygame.K_RIGHT]:
        x = top_img_rect.centerx + dx
        top_img_rect.centerx = x
        
    # TOP IMAGE ANGLE
    if keys[pygame.K_COMMA]: # < arrow
        top_angle += 0.5
        change_top_scale = True 
    if keys[pygame.K_PERIOD]:  # > arrow
        top_angle -= 0.5
        change_top_scale = True
    
    # Scale and rotate images
    if change_top_scale:
        #top_transformed_img = pygame.transform.rotozoom(top_img_svg, top_angle, top_scale)
        top_transformed_img = pygame.transform.rotozoom(top_img_svg, top_angle, top_scale)
        top_img_rect = top_transformed_img.get_rect()
        top_img_rect.center = (x,y) # latest x,y position
        change_top_scale = False
        
    if change_btm_scale: 
        btm_transformed_img = pygame.transform.rotozoom(btm_img_svg, 0, btm_scale)
        btm_x, btm_y = btm_img_rect.center # get old center coords
        btm_img_rect = btm_transformed_img.get_rect()
        btm_img_rect.center = (btm_x,btm_y)
        change_btm_scale = False
   
    # Display images
    screen.blit(btm_transformed_img, btm_img_rect)
    screen.blit(top_transformed_img, top_img_rect)
        
    # Update position of top image based on mouse position IF the mouse pos has changed
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if mouse_pos_last[0] != mouse_x or mouse_pos_last[1] != mouse_y :
        x = mouse_x
        y = mouse_y
        top_img_rect.center = (x, y)
        mouse_pos_last = [mouse_x,mouse_y]

    if show_FPS:
        display_fps()
    

    pygame.display.update()
    fpsClock.tick(FPS)

