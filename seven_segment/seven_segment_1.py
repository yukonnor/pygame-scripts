'''
Pretty close:
[[[20, 9], [30, 0], [114, 0], [124, 9], [109, 22], [34, 22]], [[128, 14], [137, 26], [136, 92], [127, 105], [111, 92], [114, 26]], [[124, 111], [134, 126], [132, 200], [122, 212], [106, 196], [108, 126]], [[9, 214], [27, 200], [102, 200], [119, 217], [110, 224], [18, 224]], [[12, 112], [26, 126], [24, 196], [6, 209], [0, 200], [2, 122]], [[16, 14], [30, 27], [28, 93], [10, 105], [4, 96], [6, 22]], [[16, 108], [30, 98], [107, 98], [121, 108], [107, 120], [30, 120]]]

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
from random import choice

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

# Seven Segment Display is ~ 160 x 240
seven_segment_coords = [[[20, 9], [30, 0], [114, 0], [124, 9], [109, 22], [34, 22]], 
                        [[128, 14], [137, 26], [136, 92], [127, 105], [111, 92], [114, 26]], 
                        [[124, 111], [134, 126], [132, 200], [122, 212], [106, 196], [108, 126]], 
                        [[9, 214], [27, 200], [102, 200], [119, 217], [110, 224], [18, 224]], 
                        [[12, 112], [26, 126], [24, 196], [6, 209], [0, 200], [2, 122]], 
                        [[16, 14], [30, 27], [28, 93], [10, 105], [4, 96], [6, 22]], 
                        [[16, 108], [30, 98], [107, 98], [121, 108], [107, 120], [30, 120]]]

# Seven segment values:
numerical_values = [[True, True, True, True, True, True, False],
                    [False, True, True, False, False, False, False],
                    [True, True, False, True, True, False, False],
                    [True, True, True, True, False, False, True],
                    [False, True, True, False, False, True, True],
                    [True, False, True, True, False, True, True],
                    [True, False, True, True, True, True, True],
                    [True, True, True, False, False, False, False],
                    [True, True, True, True, True, True, True],
                    [True, True, True, True, False, True, True]]

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

def draw_seven_segment(segment_states = [True, True, True, True, True, True, True], color = colors.YELLOW, xy = [0,0]):
    '''
    At top left corner x,y draw a seven segment display. Active segments will be set to True.
    Active segment polygon will be filled with `color`. Inactive will be black. 
    '''
    new_seven_segment_coords = []

    for i in range(7):

        polygon_coords = []

        for j in range(6):
            coord = [seven_segment_coords[i][j][0] + xy[0], seven_segment_coords[i][j][1] + xy[1]]
            polygon_coords.append(coord)
       
        new_seven_segment_coords.append(polygon_coords)

    for i in range(7):
        if segment_states[i]:
            pygame.draw.polygon(gameDisplay, color, new_seven_segment_coords[i], 0)          # if segment active, fill will color
            #pygame.draw.polygon(gameDisplay, colors.WHITE, new_seven_segment_coords[i], 2)  # draw border
        else:
            pass
            #pygame.draw.polygon(gameDisplay, colors.BLACK, new_seven_segment_coords[i], 0)  # fill all polygons
            #pygame.draw.polygon(gameDisplay, colors.WHITE, new_seven_segment_coords[i], 2)  # draw all polygon border
    
        
def randomize():
    values = [choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False])]
    return values

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
            
    # Move if a key is continually pressed down
    keys_pressed = pygame.key.get_pressed()

    random_segments = randomize()
    #print(segment_states)

    draw_grid() 
    draw_seven_segment(numerical_values[8])  
    #draw_seven_segment(random_segments, colors.YELLOW, [160,0])
    


    sleep(.3)
    pygame.display.update()
