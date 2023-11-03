'''
Pretty close:
[[[200, 229], [210, 220], [294, 220], [304, 229], [289, 242], [214, 242]], [[308, 234], [317, 246], [316, 312], [307, 325], [291, 312], [294, 246]], [[304, 331], [314, 346], [312, 420], [302, 432], [286, 416], [288, 346]], [[189, 434], [207, 420], [282, 420], [299, 437], [290, 444], [198, 444]], [[192, 332], [206, 346], [204, 416], [186, 429], [180, 420], [182, 342]], [[196, 234], [210, 247], [208, 313], [190, 325], [184, 316], [186, 242]], [[196, 328], [210, 318], [287, 318], [301, 328], [287, 340], [210, 340]]]

Todo:
- make a way to change the position of a polygon's points in real time
  - TAB to focus on next polygon to adjust
  - Active polygon shows: red dots on points, green dot on point actively beeing updated
  - Number keys to select which point is being edited
  - Arrow keys to adjust position of active point
  - Print the coords of the polygon when the position changes

'''


import pygame

from pygame.constants import NUMEVENTS, WINDOWHITTEST
import colors
from time import sleep

XRES = 800
YRES = 600
XMID = int(XRES / 2)
YMID = int(YRES / 2)

pygame.init()
gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.BLACK)
myfont = pygame.font.SysFont("monospace", 15)


NUM_POLYGONS = 7
SCRATCH_START = False #   if true start from scratch
MOVE_AMNT = 1 
polygons = []
active_polygon = 0
active_point = 0


if SCRATCH_START:
    for i in range(NUM_POLYGONS):
        point_0 = [200 + i*6,YMID + i*6]
        point_1 = [210 + i*6,YMID-10 + i*6]
        point_2 = [290 + i*6,YMID-10 + i*6]
        point_3 = [300 + i*6,YMID + i*6]
        point_4 = [285 + i*6,YMID+12 + i*6]
        point_5 = [215 + i*6,YMID+12 + i*6]
        
        polygons.append([point_0, point_1, point_2, point_3, point_4, point_5])
else:
    # enter starting coordinates
    polygons = [[[200, 229], [210, 220], [294, 220], [304, 229], [289, 242], [214, 242]], [[308, 234], [317, 246], [316, 312], [307, 325], [291, 312], [294, 246]], [[304, 331], [314, 346], [312, 420], [302, 432], [286, 416], [288, 346]], [[189, 434], [207, 420], [282, 420], [299, 437], [290, 444], [198, 444]], [[192, 332], [206, 346], [204, 416], [186, 429], [180, 420], [182, 342]], [[196, 234], [210, 247], [208, 313], [190, 325], [184, 316], [186, 242]], [[196, 328], [210, 318], [287, 318], [301, 328], [287, 340], [210, 340]]]


print(polygons)

def draw_segment(polygon_coords):
  
    # points drawn clockwise
    pygame.draw.polygon(gameDisplay, colors.BLACK, polygon_coords, 0)  # fill polygon
    pygame.draw.polygon(gameDisplay, colors.WHITE, polygon_coords, 2)  # draw polygon border

def draw_active_polygon_points(polygon_coords, active_point = 0):
    
    for point in range(len(polygon_coords)):
        if point == active_point:
            pygame.draw.circle(gameDisplay, colors.GREEN, polygon_coords[point], 2)
        else:
            pygame.draw.circle(gameDisplay, colors.RED, polygon_coords[point], 2)


def draw_grid():
  # draw vertical lines
  x_pos = 0
  for i in range(int(XRES/10)):
      pygame.draw.line(gameDisplay, colors.GRAY, (x_pos, 0), (x_pos,YRES))
      x_pos += 10

  y_pos = 0
  for i in range(int(YRES/10)):
      pygame.draw.line(gameDisplay, colors.GRAY, (0, y_pos), (XRES,y_pos))
      y_pos += 10

###############

def draw_seven_segment(active_polygon):
    for i in range(NUM_POLYGONS):
        draw_segment(polygons[i])

    draw_active_polygon_points(polygons[active_polygon], active_point)


################
# SETUP CONFIG #
################




while True:

    gameDisplay.fill(colors.BLACK)     # clear screen 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                pass

            if event.key == pygame.K_TAB:
                if active_polygon == (NUM_POLYGONS - 1):
                    active_polygon = 0
                else:
                    active_polygon += 1

                print("\nPrinting active polygone number!")
                print(active_polygon)    

            if event.key == pygame.K_LSHIFT:
                if active_point == 5:
                    active_point = 0
                else:
                    active_point += 1
            
            if event.key == pygame.K_p:
                print("\nPrinting polygon coordinates!")
                print(polygons)
            
    # Move if a key is continually pressed down
    keys_pressed = pygame.key.get_pressed()

    if keys_pressed[pygame.K_UP] and not keys_pressed[pygame.K_SPACE]:
        polygons[active_polygon][active_point][1] -= MOVE_AMNT
    
    if keys_pressed[pygame.K_DOWN] and not keys_pressed[pygame.K_SPACE]:
        polygons[active_polygon][active_point][1] += MOVE_AMNT
    
    if keys_pressed[pygame.K_LEFT] and not keys_pressed[pygame.K_SPACE]:
        polygons[active_polygon][active_point][0] -= MOVE_AMNT
    
    if keys_pressed[pygame.K_RIGHT] and not keys_pressed[pygame.K_SPACE]:
        polygons[active_polygon][active_point][0] += MOVE_AMNT

    # move entire seven segment:
    if keys_pressed[pygame.K_UP] and keys_pressed[pygame.K_SPACE]:
        for i in range(NUM_POLYGONS):
            for point in range(len(polygons[i])):
                polygons[i][point][1] -= 2
    
    if keys_pressed[pygame.K_DOWN] and keys_pressed[pygame.K_SPACE]:
        for i in range(NUM_POLYGONS):
            for point in range(len(polygons[i])):
                polygons[i][point][1] += 2
    
    if keys_pressed[pygame.K_LEFT] and keys_pressed[pygame.K_SPACE]:
        for i in range(NUM_POLYGONS):
            for point in range(len(polygons[i])):
                polygons[i][point][0] -= 2
    
    if keys_pressed[pygame.K_RIGHT] and keys_pressed[pygame.K_SPACE]:
        for i in range(NUM_POLYGONS):
            for point in range(len(polygons[i])):
                polygons[i][point][0] += 2
    
    

    draw_grid()   
    draw_seven_segment(active_polygon)
    


    sleep(.1)
    pygame.display.update()
