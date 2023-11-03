
'''
This scetch:
- Imports svg moire template images
- Has ability to colorize, scale, reposiition and rotate images to create moire patterns
- Animates the moire patterns:
  - Animation Mode: Automatically animates the top image (position and angle) using (TODO X predefined animation patterns) to give some hands free moires
  - Manual Mode: 
    - Manually adjust POSITION of bottom image using W, S, A, D keys
    - Manually adjust SCALE of bottom image (preferred to scaling top image) using BRACKET keys
    
    - Manually adjust POSITION of top image using UP, DOWN, LEFT, RIGHT keys
    - Mansuall adjust POSITION of top image using the mouse position to give a more organic experience 
      - TODO: Mouse first has to 'lock on' to an area near the center of the image before it starts to move it
        to avoid jumping when mouse comes to the screen.
    - Manually adjust the ANGLE of the top image using the < and > keys

SVG NOTES:
- ALL SVG IMAGES should use same dimensions (Currently 1000x1000 square)
- The width and height define the CANVAS size (AKA VIEW PORT)
  - The canvas size should be wide and tall enough for the svg img to fully fit at any angle (if square, canvas size should be at least 1.4x the square's width)
- The viewbox defines the position and scale of the drawing within the frame of the canvas
  - If svg width = 100 and the viewbox width = 50, a rect with side = 50 will take up 100% of the canvas
- If the svg width is 1.4x the original square width of the svg, to maintain the same proportional size you will need to "zoom" in a bit in the code


TODO:
- Add animation patterns and figure how to turn on/off and cycle through animation patterns
  - Maybe record and loop movements? 
- If you want to scale top image to be larger or smaller while remaining managegable size, play with pre-scaled different versions (s, m, l) of the same image that can be loaded
- Organize the code (constants at top, easier to switch to fullscreen)
- Create 'denser' dotmatrix images

'''

import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from moire_colors  import *  # import the color variables from local file
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

FILEPATH = '/Users/concon/pygame-scripts/moire/images/'
SVG_NAMES = ['cirlces.svg', 'lines_0.svg', 'lines_1.svg', 'radial_angles_0.svg', 'halftone_linear_3.svg', 'halftone_linear_4.svg','halftone_donut.svg','halftone_rings.svg']
SVG_WIDTH = 1000
SVG_HEIGHT = 1000
COLORS = [BLACK, WHITE, RED_ORANGE, GREEN, BLUE, PURPLE, YELLOW, ORANGE]
NUM_COLORS = len(COLORS)


# Load and Scale SVG Images to a Pygame Surface:
# NOTE: Removing rotation from function in this script as rotating with rotozoom. Becuase no rotation we can remove viewport buffer.
def load_svg(filename, color = None):      
    
    svg_string = open(filename, "rt").read()  # original SVG  
    
    # Replace black with color provided
    svg_string = svg_string.replace('black', f'rgb{color}')
    svg_string = svg_string.replace('#000000', f'rgb{color}') # if color defined via hex
    
    #print(svg_string)
   
    return pygame.image.load(io.BytesIO(svg_string.encode())).convert_alpha()


def change_image(img_num, scale, color, angle):
    filename = FILEPATH + SVG_NAMES[img_num]
    img_surface = load_svg(filename, color)
    transformed_img_surface = pygame.transform.rotozoom(img_surface, angle, scale)
    
    return img_surface, transformed_img_surface


def display_fps():
    font = pygame.font.SysFont("Arial", 24)
    fps_string = "FPS = " + str(int(fpsClock.get_fps()))
    text_to_show = font.render(fps_string, 0, WHITE)
    pygame.draw.rect(screen, BLACK, (0,0,130,40))
    screen.blit(text_to_show, (5,5))


########################################
# Startup Sequence
########################################

btm_img_num = 7
btm_filepath = FILEPATH + SVG_NAMES[btm_img_num]
btm_color_index = 4
btm_color = COLORS[4] # blue

btm_img_svg = load_svg(btm_filepath, btm_color)
btm_img_rect = btm_img_svg.get_rect() # this doesn't appear to ingest the scaleed size, so have to adjust
btm_img_rect.center = (XMID, YMID)  # center the img on the screen

top_img_num = 7
top_filename = FILEPATH + SVG_NAMES[top_img_num]
top_color_index = 4
top_color = COLORS[4] # blue

top_img_svg = load_svg(top_filename, top_color)
top_img_rect = top_img_svg.get_rect()
top_img_rect.center = (XMID, YMID) 

# set mouse cursor to be invisible
pygame.mouse.set_visible(False)
mouse_pos_last = [0,0]

# Scale & position variables for real time scaling during the sketch
top_x = XMID
top_y = YMID
btm_x = XMID
btm_y = YMID
dx = 2
dy = 2
top_angle = 0
change_btm_scale = False
change_top_scale = False
btm_scale = 1
top_scale = 1
btm_transformed_img = btm_img_svg
top_transformed_img = top_img_svg


bg_color = BLACK
bg_color_index = 0

show_FPS = False

########################################
# Main Game Loop
########################################
while True:
    screen.fill(bg_color)     # clear screen 

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
            # SCALE TOP IMAGE: 
            if event.key == pygame.K_MINUS:
                top_scale -= .1
                change_top_scale = True  
            if event.key == pygame.K_EQUALS: # ie the +PLUS key
                top_scale += .1
                change_top_scale = True 
            # SCALE BOTTOM IMAGE
            if event.key == pygame.K_LEFTBRACKET:
                btm_scale -= .1
                change_btm_scale = True 
            if event.key == pygame.K_RIGHTBRACKET:
                btm_scale += .1
                change_btm_scale = True       
            # CHANGE TOP IMAGE   
            if event.unicode in ['1','2','3','4','5','6','7','8','9','0']:
                top_img_num = ['1','2','3','4','5','6','7','8','9','0'].index(event.unicode)
                top_img_svg, top_transformed_img = change_image(top_img_num, top_scale, top_color, top_angle)
                top_img_rect = top_transformed_img.get_rect()
                top_img_rect.center = (top_x,top_y) # latest x,y position
            # CHANGE BTM IMAGE  (Shift + number keys)
            if event.unicode in ['!','@','#','$','%','^','&','*','(',')']:
                btm_img_num = ['!','@','#','$','%','^','&','*','(',')'].index(event.unicode)
                btm_img_svg, btm_transformed_img = change_image(btm_img_num, btm_scale, btm_color, 0)
                btm_img_rect = btm_transformed_img.get_rect()
                btm_img_rect.center = (btm_x,btm_y) # latest x,y position
            # BG COLOR CHANGE
            if event.key == pygame.K_RSHIFT:
                bg_color_index += 1  
                bg_color = COLORS[bg_color_index % NUM_COLORS]
            # BTM COLOR CHANGE
            if event.key == pygame.K_RETURN:
                btm_color_index += 1  
                btm_color = COLORS[btm_color_index % NUM_COLORS]  
                btm_img_svg, btm_transformed_img = change_image(btm_img_num, btm_scale, btm_color, 0)
                btm_img_rect = btm_transformed_img.get_rect()
                btm_img_rect.center = (btm_x,btm_y)
            # TOP COLOR CHANGE
            if event.key == pygame.K_BACKSLASH:
                top_color_index += 1  
                top_color = COLORS[top_color_index % NUM_COLORS]  
                print("New color for top image:", top_color_index, top_color)
                top_img_svg, top_transformed_img = change_image(top_img_num, top_scale, top_color, top_angle)
                top_img_rect = top_transformed_img.get_rect()
                top_img_rect.center = (top_x,top_y)
            

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
        top_y = top_img_rect.centery - dy
        top_img_rect.centery = top_y
    if keys[pygame.K_DOWN]:
        top_y = top_img_rect.centery + dy
        top_img_rect.centery = top_y
    if keys[pygame.K_LEFT]:
        top_x = top_img_rect.centerx - dx
        top_img_rect.centerx = top_x
    if keys[pygame.K_RIGHT]:
        top_x = top_img_rect.centerx + dx
        top_img_rect.centerx = top_x
        
    # TOP IMAGE ANGLE
    if keys[pygame.K_COMMA]: # < arrow
        top_angle += 0.5
        change_top_scale = True 
    if keys[pygame.K_PERIOD]:  # > arrow
        top_angle -= 0.5
        change_top_scale = True
    if keys[pygame.K_COMMA] and keys[pygame.K_LSHIFT]: # < arrow + shift
        top_angle += 5
        change_top_scale = True 
    if keys[pygame.K_PERIOD] and keys[pygame.K_LSHIFT]:  # > arrow + shift
        top_angle -= 5
        change_top_scale = True
        
        
    # Scale and rotate images
    if change_top_scale:
        #print("TOP SCALE:", top_scale, " TOP ANGLE:", top_angle)
        top_transformed_img = pygame.transform.rotozoom(top_img_svg, top_angle, top_scale)
        top_img_rect = top_transformed_img.get_rect()
        top_img_rect.center = (top_x,top_y) # latest x,y position
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
        top_x = mouse_x
        top_y = mouse_y
        top_img_rect.center = (top_x, top_y)
        mouse_pos_last = [mouse_x,mouse_y]

    if show_FPS:
        display_fps()
    

    pygame.display.update()
    fpsClock.tick(FPS)

