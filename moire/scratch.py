
'''
This scetch:
- Imports svg moire template images and scales them to the size you want
  - TODO: Scale real time during the sketch to animate the size?
- Either:
  - Automatically animates the top image to give some hands free moires
  - Manually adjusts the BOTTOM image with arrow keys
  - OR use the mouse position to move the TOP image to give a more controlled experience 
    - TODO: Mouse first has to 'lock on' to an area near the center of the image before it starts to move it
      to avoid jumping when mouse comes to the screen.

SVG NOTES:
- The width and height define the CANVAS size (AKA VIEW PORT)
  - The canvas size should be wide and tall enough for the svg img to fully fit at any angle (if square, canvas size should be at least 1.4x the square's width)
- The viewbox defines the position and scale of the drawing within the frame of the canvas
  - If svg width = 100 and the viewbox width = 50, a rect with side = 50 will take up 100% of the canvas
- If the svg width is 1.4x the original square width of the svg, to maintain the same proportional size you will need to "zoom" in a bit in the code


TODO:
- Remove viewbox?
- To rotate by center while keeping the full image (not getting cutoff), need to adjust rotation pivot point as it rotates
'''

import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors import *         # import the color variables from local file
import io                    # to manipulate text properties of SVG images
import time
from line_profiler import LineProfiler


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

# Load and Scale SVG Images to a Pygame Surface:
def load_and_scale_svg(svg_string, og_svg_width, og_svg_height, scale, color = None, angle = None):        
    # as we're multiplying things by default by 1.5 to support rotation (max length of diagonal), to mainain the original scale (1) we need to multiply by 1.5
    ##t0 = time.time()

    scale = scale * 1.5
    
    # update the width of the viewport to be wide enough to see full image when rotating
    svg_string = svg_string.replace(f'width="{og_svg_width}"', f'width="{og_svg_width * 1.5 * scale}"', 1)
    svg_string = svg_string.replace(f'height="{og_svg_height}"', f'height="{og_svg_height * 1.5 * scale}"', 1)
        
    # because we're updating the viewport, we need to update the viewbox to maintain the same scale
    viewbox_offset = -1 * (((og_svg_width * 1.5) - og_svg_width)/2)
    svg_string = svg_string.replace(f'viewBox="0 0 {og_svg_width} {og_svg_width}"', f'viewBox="{viewbox_offset} {viewbox_offset} {og_svg_width*1.5} {og_svg_width*1.5}"', 1)
    
    #t1 = time.time()
    #total_time = t1 - t0
    #print("Time to replace Svgstring scale parts:", total_time)
    
    
    # Replace black with color provided
    svg_string = svg_string.replace('black', f'{color}')
    
    # if an angle is provided, attempt to rotate the svg by that angle
    if angle:
        #t0 = time.time()
        # rotate around image's center point
        mid_x = og_svg_width / 2
        mid_y = og_svg_height / 2
        svg_string = svg_string.replace(f'rotate(0)', f'rotate({angle}, {mid_x}, {mid_y})', 1)
        #t1 = time.time()
        #total_time = t1 - t0
        #print("Time to replace SVG string rotation parts:", total_time)
    
    #t0 = time.time()
    converted_svg_string = io.BytesIO(svg_string.encode())
    #t1 = time.time()
    #total_time = t1 - t0
    #print("Time to convert SVG string:", total_time)
    
    #t0 = time.time()
    image_surface = pygame.image.load(converted_svg_string)
    #t1 = time.time()
    #print("Time create SVG img surface:", total_time, '\n')
    
    return image_surface


def display_fps():
    "Data that will be rendered and blitted in _display"
    font = pygame.font.SysFont("Arial", 24)
    fps_string = "FPS = " + str(int(fpsClock.get_fps()))
    text_to_show = font.render(fps_string, 0, WHITE)
    pygame.draw.rect(screen, BLACK, (0,0,130,40))
    screen.blit(text_to_show, (5,5))


##############################
# Startup Sequence
##############################

FILEPATH = '/Users/concon/pygame-scripts/moire/'
SVG_NAMES = ['Cirlces.svg', 'Lines.svg', 'Radial Circle.svg', 'dot_matrix_3.svg']
svg_scale = 1

btm_filepath = FILEPATH + SVG_NAMES[3]
btm_svg_string = open(btm_filepath, "rt").read()  # original SVG
btm_img_og_width = 1000
btm_img_og_height = 1000
btm_color = 'blue'

btm_img_svg = load_and_scale_svg(btm_svg_string, btm_img_og_width, btm_img_og_height, svg_scale, btm_color)
btm_img_rect = btm_img_svg.get_rect() # this doesn't appear to ingest the scaleed size, so have to adjust
#btm_img_rect.size = (btm_img_rect.width * svg_scale, btm_img_rect.height * svg_scale) # adjusting surface size here
btm_img_rect.center = (XMID, YMID)  # center the img on the screen
print("Bottom imgage rect:", btm_img_rect)

top_filename = FILEPATH + SVG_NAMES[3]
top_svg_string = open(top_filename, "rt").read()  # original SVG
top_img_og_width = 1000
top_img_og_height = 1000
top_color = 'blue'
top_angle = 180

top_img_svg = load_and_scale_svg(top_svg_string, top_img_og_width, top_img_og_height, svg_scale, top_color, top_angle)
top_img_rect = top_img_svg.get_rect()
#top_img_rect.size = (top_img_rect.width * svg_scale, top_img_rect.height * svg_scale)
x = XMID
y = YMID
top_img_rect.center = (x, y) 

# set mouse cursor to be invisible
pygame.mouse.set_visible(False)
mouse_pos_last = [0,0]

# Scale variables for real time scaling during the sketch
dx = 2
dy = 2
change_scale = False
btm_scale = svg_scale
top_scale = svg_scale
btm_transformed_img = btm_img_svg
top_transformed_img = top_img_svg

show_FPS = True


lprofiler = LineProfiler()
lp_wrapper = lprofiler(load_and_scale_svg)


print("Game loop starting...")

##############################
# Main Game Loop
##############################
while True:
    screen.fill(RED)     # clear screen 

    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                lprofiler.print_stats()
                pygame.quit()
                quit()
            if event.key == pygame.K_f:
                show_FPS = not show_FPS
            if event.key == pygame.K_UP:
                top_scale += .1
                change_scale = True  # only change the scale when it changes to avoid slowdowns
            if event.key == pygame.K_DOWN:
                top_scale -= .1
                change_scale = True             

     # Checking pressed / holds down keys
    keys = pygame.key.get_pressed()  
    if keys[pygame.K_UP]:
        btm_img_rect.centery -= dy 
    if keys[pygame.K_DOWN]:
        btm_img_rect.centery += dy 
    if keys[pygame.K_LEFT]:
        btm_img_rect.centerx -= dx
    if keys[pygame.K_RIGHT]:
        btm_img_rect.centerx += dx 
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
        top_angle -= 0.5
        change_scale = True  # only change the scale when it changes to avoid slowdowns
    if keys[pygame.K_PERIOD]:  # > arrow
        top_angle += 0.5
        change_scale = True
    
    # Scale and rotate images
    if change_scale:
        #print("Scale changing to:", top_scale, "Angle changing to:", top_angle) 
        
        #t0 = time.time()
        top_transformed_img = lp_wrapper(top_svg_string, top_img_og_width, top_img_og_height, top_scale, top_color, top_angle)  # Calls function being wrapped    # load_and_scale_svg(top_svg_string, top_img_og_width, top_img_og_height, top_scale, top_color, top_angle) # removed top_angle
        #t1 = time.time()
        #total_time = t1 - t0
        #print("Time run scale and convert function:", total_time, '\n')
        
        top_img_rect = top_transformed_img.get_rect()
        top_img_rect.center = (x,y) # latest x,y position
        change_scale = False
   
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

