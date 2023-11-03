import pygame
import colors
from time import sleep
import random
import math

# Amazon neopixel ring counts: 8, 16, 24, 35, 45
# Amazon neopixe ring radius (mm): 11, 21, 32, 44, 56 
# Note: pygame-ce has a blur function...could be cool to see what it'd look like diffused

XRES = 800
YRES = 800

TOTAL_PIXEL_COUNT = 120 # 16, 24, 35, 45
S_PIXEL_COUNT = 16
M_PIXEL_COUNT = 24
L_PIXEL_COUNT = 35
XL_PIXEL_COUNT = 45
M_PIXEL_START = S_PIXEL_COUNT # 16
M_PIXEL_END = M_PIXEL_START + M_PIXEL_COUNT # 40
L_PIXEL_START = M_PIXEL_START + M_PIXEL_COUNT # 40
L_PIXEL_END = L_PIXEL_START + L_PIXEL_COUNT   # 75
XL_PIXEL_START = L_PIXEL_START + L_PIXEL_COUNT # 75 
XL_PIXEL_END = XL_PIXEL_START + XL_PIXEL_COUNT # 120

PIXEL_RADIUS = 10
RADIUS_MULT = 3
S_RADIUS = 21 * RADIUS_MULT
M_RADIUS = 32 * RADIUS_MULT
L_RADIUS = 44 * RADIUS_MULT
XL_RADIUS = 56 * RADIUS_MULT


gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.DARK_GRAY)

pixel_colors = []
shifted_pixel_colors = [] # pixel colors after they have been shifted
final_pixel_colors = [] # pixel colors after they have been shifted and faded
shift_amts = [0,0,0,0] # Shift amount (pos/neg steps) for each circle
shift_positions = [1,1,1,-1] # Shift position for each circle
fade_mults = [1.0, 1.0, 1.0, 1.0]  # [s,m,l,xl] between 0.0 (black) and 1.0
 

#initialize pixel colors
for n in range(TOTAL_PIXEL_COUNT):
    pixel_colors.append([0,0,0])
    shifted_pixel_colors.append([0,0,0])
    final_pixel_colors.append([0,0,0])


#######

def set_pixel_color(n, red, green, blue):
    # This is the final step. This assigns the final pixel colors to the real world pixels.
    global final_pixel_colors # not ideal, but doing so to make program better match the neopixel library
    final_pixel_colors[n] = [red, green, blue]
    
def fade_pixel_colors(shifted_color_list, fade_amount):
    # take the shifted pixel colors, apply the fade amount and tell the system to set the colors of the IRL pixels
    global final_pixel_colors
    for i in range(0,S_PIXEL_COUNT):
        r = shifted_color_list[i][0] * fade_amount[0]
        g = shifted_color_list[i][1] * fade_amount[0]
        b = shifted_color_list[i][2] * fade_amount[0]
        final_pixel_colors[i] = [r, g, b]
    for i in range(M_PIXEL_START,M_PIXEL_END):
        r = shifted_color_list[i][0] * fade_amount[1]
        g = shifted_color_list[i][1] * fade_amount[1]
        b = shifted_color_list[i][2] * fade_amount[1]
        final_pixel_colors[i] = [r, g, b]
    for i in range(L_PIXEL_START,L_PIXEL_END):
        r = shifted_color_list[i][0] * fade_amount[2]
        g = shifted_color_list[i][1] * fade_amount[2]
        b = shifted_color_list[i][2] * fade_amount[2]
        final_pixel_colors[i] = [r, g, b]
    for i in range(XL_PIXEL_START,XL_PIXEL_END):
        r = shifted_color_list[i][0] * fade_amount[3]
        g = shifted_color_list[i][1] * fade_amount[3]
        b = shifted_color_list[i][2] * fade_amount[3]
        final_pixel_colors[i] = [r, g, b]
        

def draw_neopixel_circles(final_pixel_colors, circle = 'all'):
    # define values for each circle type
    if circle == 'all':
        pixel_range = [[0, S_PIXEL_COUNT], [M_PIXEL_START, M_PIXEL_END], [L_PIXEL_START, L_PIXEL_END], [XL_PIXEL_START, XL_PIXEL_END]]
        pixel_count = [S_PIXEL_COUNT, M_PIXEL_COUNT, L_PIXEL_COUNT, XL_PIXEL_COUNT]    
        radius = [S_RADIUS, M_RADIUS, L_RADIUS, XL_RADIUS]
    elif circle == 's':
        pixel_range = [[0, S_PIXEL_COUNT]]
        pixel_count = [S_PIXEL_COUNT]
        radius = [S_RADIUS]
    elif circle == 'm':
        pixel_range = [[M_PIXEL_START, M_PIXEL_END]]
        pixel_count = [M_PIXEL_COUNT]
        radius = [M_RADIUS]
    elif circle == 'l':
        pixel_range = [[L_PIXEL_START, L_PIXEL_END]]
        pixel_count = [L_PIXEL_COUNT]
        radius = [L_RADIUS]
    elif circle == 'xl':
        pixel_range = [[XL_PIXEL_START, XL_PIXEL_END]]
        pixel_count = [XL_PIXEL_COUNT]
        radius = [XL_RADIUS]
    
    for i,px_range in enumerate(pixel_range):
        angle_per_pixel = 360 / pixel_count[i]
        angle = angle_per_pixel * (pixel_count[i]/2 - 1) # start at an angle offset so that pixel 0 appears at top of each circle
        
        for j in range(px_range[0],px_range[1]):
            angle = angle + angle_per_pixel
            radians = angle * (3.1415/180) # pi / 180
            x = (XRES/2) + radius[i] * math.sin(radians)
            y = (YRES/2) + radius[i] * math.cos(radians)
            color = tuple(final_pixel_colors[j])
            pygame.draw.circle(gameDisplay, color, (x,y), PIXEL_RADIUS)
        
def pixels_per_color(circle, num_colors):
    # helper function to divide the number of pixels in a given circle by the number of colors we want on the circle
    pixels_per_color = 0
    if circle == 's':
        pixels_per_color = S_PIXEL_COUNT / num_colors 
    elif circle == 'm':
        pixels_per_color = M_PIXEL_COUNT / num_colors 
    elif circle == 'l':
        pixels_per_color = L_PIXEL_COUNT / num_colors 
    elif circle == 'xl':
        pixels_per_color = XL_PIXEL_COUNT / num_colors 
    return int(round(pixels_per_color))

def set_gradient(circle, color_list):
    # find how many colors there are 
    num_colors = len(color_list)
    count_per_color = pixels_per_color(circle, num_colors)
    global pixel_colors
    global fade_mults
    
    # define offset for each circle type
    if circle == 's':
        circle_offset = 0
    elif circle == 'm':
        circle_offset =  M_PIXEL_START
    elif circle == 'l':
        circle_offset =  L_PIXEL_START
    elif circle == 'xl':
        circle_offset =  XL_PIXEL_START
   
    for color in range(num_colors):            
        current_range = [(color * count_per_color) + circle_offset, ((color + 1) * count_per_color) + circle_offset]
        color_0 = list(color_list[color])
        color_1 = list(color_list[(color+1) % num_colors])
        pixel_color = color_0.copy()
        for pixel in range(current_range[0],current_range[1]): 
            # define pixel colors: 
            pixel_colors[pixel] = [pixel_color[0], pixel_color[1], pixel_color[2]] 
            # find next color in the gradient: 
            pixel_color[0] += int((color_1[0]-color_0[0]) / count_per_color)
            pixel_color[1] += int((color_1[1]-color_0[1]) / count_per_color)
            pixel_color[2] += int((color_1[2]-color_0[2]) / count_per_color)
     

def update_shift_positions(shift_amt_list, shift_positions):
    circle_pixel_counts = [S_PIXEL_COUNT, M_PIXEL_COUNT, L_PIXEL_COUNT, XL_PIXEL_COUNT]
    for i, pixel_count in enumerate(circle_pixel_counts):
        shift_steps = shift_amt_list[i]
        shift_positions[i] = (shift_positions[i] + shift_steps) % pixel_count
        
    return shift_positions

def shift_colors(shift_positions, color_list):
    
    global shifted_pixel_colors
    
    # TODO: If slow, could possibly only shift if a circle is shifting but if we do that we'll need to somehow initizel the shifted list each time the color changes
    for i in range(S_PIXEL_COUNT):
        index_to_get = 0 + ((i + shift_positions[0]) % S_PIXEL_COUNT)
        shifted_pixel_colors[i + 0] = color_list[index_to_get]
    for i in range(M_PIXEL_COUNT):
        index_to_get = M_PIXEL_START + ((i + shift_positions[1]) % M_PIXEL_COUNT)
        shifted_pixel_colors[i + M_PIXEL_START] = color_list[index_to_get]
    for i in range(L_PIXEL_COUNT):
        index_to_get = L_PIXEL_START + ((i + shift_positions[2]) % L_PIXEL_COUNT)
        shifted_pixel_colors[i + L_PIXEL_START] = color_list[index_to_get]
    for i in range(XL_PIXEL_COUNT):
        # 45 pixels, 75 - 120
        index_to_get = XL_PIXEL_START + ((i + shift_positions[3]) % XL_PIXEL_COUNT)
        #print(i, shift_positions[3], (i + shift_positions[3]), index_to_get)
        shifted_pixel_colors[i + XL_PIXEL_START] = color_list[index_to_get]
        

def set_fade_amt(circle, new_fade_mult):
    #TODO: How do you want this to work? Fade to black is easy but do you want to be able to fade back to a different set of colors? 
    # Fade is like a gradient through time whereas the gradient function I have now is gradient accross space
    # Also trick to do if circle is spinning already. 
    # May be easies to do a high level multiplier done when setting the 'final color' (final color = current color * fade amount)
    global fade_mults

    fade_mults[circle] = new_fade_mult

def set_color_blocks():
    pass


loop_count = 0
ramp_length = 5
mode = ''
run_at_start = True
live_color = [200,0,200]

while True:

    gameDisplay.fill(colors.DARK_GRAY)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                ramp_length += 1
            if event.key == pygame.K_DOWN:
                ramp_length -= 1
            if event.key == pygame.K_s:
                mode = 'shift'   
            if event.key == pygame.K_c:
                mode = 'define colors'  
            if event.key == pygame.K_f:
                mode = 'fade'  
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
    
    # Get currently pressed keys
    keys = pygame.key.get_pressed()    
    
    # ACTIONS TO DO ONCE AT START (CURRENTLY SETTING COLORS)
    if run_at_start:
        color = tuple(live_color)
        set_gradient('s', ((0,0,0),(0,0,0),color))
        set_gradient('m', ((0,0,0),(0,0,0),color))
        set_gradient('l', ((0,0,0),(0,0,0),color))
        set_gradient('xl', ((0,0,0),(0,0,0),color))    
        
        run_at_start = False
   
    # ACTIONS BASED ON CURRENT MODE
    if mode == 'define colors':
        color = tuple(live_color)
        set_gradient('s', ((0,0,0),(0,0,0),color))
        set_gradient('m', ((0,0,0),(0,0,0),color))
        set_gradient('l', ((0,0,0),(0,0,0),color))
        set_gradient('xl', ((0,0,0),(0,0,0),color))  
        
        if keys[pygame.K_r] and keys[pygame.K_UP]:
            live_color[0] = min(live_color[0] + 5, 255)
        if keys[pygame.K_r] and keys[pygame.K_DOWN]:
            live_color[0] = max(live_color[0] - 5, 0)
        if keys[pygame.K_g] and keys[pygame.K_UP]:
            live_color[1] = min(live_color[1] + 5, 255)
        if keys[pygame.K_g] and keys[pygame.K_DOWN]:
            live_color[1] = max(live_color[1] - 5, 0)
        if keys[pygame.K_b] and keys[pygame.K_UP]:
            live_color[2] = min(live_color[2] + 5, 255)
        if keys[pygame.K_b] and keys[pygame.K_DOWN]:
            live_color[2] = max(live_color[2] - 5, 0)
        
    elif mode == 'shift':
        
        if keys[pygame.K_1] and keys[pygame.K_UP]:
            shift_amts[0] = min(shift_amts[0] + 1, 5)
        if keys[pygame.K_1] and keys[pygame.K_DOWN]:
            shift_amts[0] = max(shift_amts[0] - 1, -5)
        if keys[pygame.K_2] and keys[pygame.K_UP]:
            shift_amts[1] = min(shift_amts[1] + 1, 5)
        if keys[pygame.K_2] and keys[pygame.K_DOWN]:
            shift_amts[1] = max(shift_amts[1] - 1, -5)
        if keys[pygame.K_3] and keys[pygame.K_UP]:
            shift_amts[2] = min(shift_amts[2] + 1, 5)
        if keys[pygame.K_3] and keys[pygame.K_DOWN]:
            shift_amts[2] = max(shift_amts[2] - 1, -5)
        if keys[pygame.K_4] and keys[pygame.K_UP]:
            shift_amts[3] = min(shift_amts[3] + 1, 5)
        if keys[pygame.K_4] and keys[pygame.K_DOWN]:
            shift_amts[3] = max(shift_amts[3] - 1, -5)    
        
    
    elif mode == 'fade':
        
        if keys[pygame.K_1] and keys[pygame.K_UP]:
            fade_mults[0] = min(fade_mults[0] + 0.1, 1)
        if keys[pygame.K_1] and keys[pygame.K_DOWN]:
            fade_mults[0] = max(fade_mults[0] - 0.1, 0)
        if keys[pygame.K_2] and keys[pygame.K_UP]:
            fade_mults[1] = min(fade_mults[1] + 0.1, 1)
        if keys[pygame.K_2] and keys[pygame.K_DOWN]:
            fade_mults[1] = max(fade_mults[1] - 0.1, 0)
        if keys[pygame.K_3] and keys[pygame.K_UP]:
            fade_mults[2] = min(fade_mults[2] + 0.1, 1)
        if keys[pygame.K_3] and keys[pygame.K_DOWN]:
            fade_mults[2] = max(fade_mults[2] - 0.1, 0)
        if keys[pygame.K_4] and keys[pygame.K_UP]:
            fade_mults[3] = min(fade_mults[3] + 0.1, 1)
        if keys[pygame.K_4] and keys[pygame.K_DOWN]:
            fade_mults[3] = max(fade_mults[3] - 0.1, 0)
        
        for i,fade in enumerate(fade_mults):
            if fade < 1:     
                set_fade_amt(i, fade)
            
    # DRAW PIXELS
    shift_positions = update_shift_positions(shift_amts, shift_positions)
    shift_colors(shift_positions, pixel_colors)
    fade_pixel_colors(shifted_pixel_colors, fade_mults)
    draw_neopixel_circles(final_pixel_colors)    
    
    sleep(.2)
    pygame.display.update()