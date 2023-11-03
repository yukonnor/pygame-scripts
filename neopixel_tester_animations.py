import pygame
import colors
from time import sleep
import random
import math

# Neopixel rings pixel counts: 12, 16, 24, 60
# Neopixel ring radius: .75, .875, 1.3, 3.1
# Note: pygame-ce has a blur function...could be cool to see what it'd look like diffused

XRES = 800
YRES = 800

PIXEL_COUNT = 96 # 12 + 24 + 60
PIXEL_RADIUS = 10

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.DARK_GRAY)

pixel_colors = []
 

#initialize pixel colors
for n in range(PIXEL_COUNT):
    pixel_colors.append([0,0,0])
    

def set_pixel_color(n, red, green, blue):
    # n: pixel number 0 - PIXEL_COUNT-1
    # rgb: 0 - 255
    global pixel_colors # not ideal, but doing so to make program better match the neopixel library
    pixel_colors[n] = [red, green, blue]

def draw_neopixel_circles(pixel_colors):
    # draw small circle (0-11)
    small_pixel_count = 12
    small_radius = 75
    angle_per_pixel = 360 / small_pixel_count
    angle = 0
    
    for i in range(0,small_pixel_count):
        angle = angle + angle_per_pixel
        radians = angle * (3.1415/180) # pi / 180
        x = (XRES/2) + small_radius * math.sin(radians)
        y = (YRES/2) + small_radius * math.cos(radians)
        color = tuple(pixel_colors[i])
        pygame.draw.circle(gameDisplay, color, (x,y), PIXEL_RADIUS)
    
    
    # draw medium circle (12-35)
    med_pixel_count = 24
    medium_radius = 130
    angle_per_pixel = 360 / med_pixel_count
    angle = 0
    
    for i in range(small_pixel_count,med_pixel_count+small_pixel_count):
        angle = angle + angle_per_pixel
        radians = angle * (3.1415/180) # pi / 180
        x = (XRES/2) + medium_radius * math.sin(radians)
        y = (YRES/2) + medium_radius * math.cos(radians)
        color = tuple(pixel_colors[i])
        pygame.draw.circle(gameDisplay, color, (x,y), PIXEL_RADIUS)
    
    # draw large circle (36-95)
    lrg_pixel_count = 60
    large_radius = 310
    angle_per_pixel = 360 / lrg_pixel_count
    angle = 0
    
    for i in range(med_pixel_count,lrg_pixel_count+med_pixel_count):
        angle = angle + angle_per_pixel
        radians = angle * (3.1415/180) # pi / 180
        x = (XRES/2) + large_radius * math.sin(radians)
        y = (YRES/2) + large_radius * math.cos(radians)
        color = tuple(pixel_colors[i])
        pygame.draw.circle(gameDisplay, color, (x,y), PIXEL_RADIUS)
        
def ramp_color(ramp_length, color):
    red = color[0]
    green = color[1]
    blue = color[2]
    
    ramp_count = 0
    ramp_color_mod_r = 0
    ramp_color_mod_g = 0
    ramp_color_mod_b = 0
    
    for pixel in range(PIXEL_COUNT):
        
        set_pixel_color(pixel, red+ramp_color_mod_r, green+ramp_color_mod_g, blue+ramp_color_mod_b)
        
        ramp_count += 1
        ramp_color_mod_r = ramp_color_mod_r - (red / ramp_length)
        ramp_color_mod_g = ramp_color_mod_g - (green / ramp_length)
        ramp_color_mod_b = ramp_color_mod_b - (blue / ramp_length)
        if ramp_count >= ramp_length:
            ramp_count = 0
            ramp_color_mod_r = 0
            ramp_color_mod_g = 0
            ramp_color_mod_b = 0

def shift_colors(shift_count, direction, pixel_colors):
    new_pixel_colors = []
    if direction == 1:
        for i in range(PIXEL_COUNT):
            new_pixel_colors.append(pixel_colors[(shift_count + i) % PIXEL_COUNT])
    
    return new_pixel_colors    

loop_count = 0
ramp_length = 5
mode = ''

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
            if event.key == pygame.K_r:
                mode = 'ramp'   
            if event.key == pygame.K_s:
                mode = 'shift'   
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    # DRAW SHAPES
    if mode == 'ramp':
        ramp_color(ramp_length, (255,0,0))
    elif mode == 'shift':
        pixel_colors = shift_colors(1, 1, pixel_colors)
    draw_neopixel_circles(pixel_colors)
    
    
    
    loop_count += 1
    if loop_count >= 10:
        loop_count = 0
    sleep(.5)
    pygame.display.update()