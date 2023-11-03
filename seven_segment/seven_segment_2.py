'''
Pretty close:
[[[20, 9], [30, 0], [114, 0], [124, 9], [109, 22], [34, 22]], [[128, 14], [137, 26], [136, 92], [127, 105], [111, 92], [114, 26]], [[124, 111], [134, 126], [132, 200], [122, 212], [106, 196], [108, 126]], [[9, 214], [27, 200], [102, 200], [119, 217], [110, 224], [18, 224]], [[12, 112], [26, 126], [24, 196], [6, 209], [0, 200], [2, 122]], [[16, 14], [30, 27], [28, 93], [10, 105], [4, 96], [6, 22]], [[16, 108], [30, 98], [107, 98], [121, 108], [107, 120], [30, 120]]]

Todo:
- make segments flow more:
    - drunk randomization of segments (can turn on if touching one of on segments, turn off if has been on for 2+ cycles, if all off pick random segment to turn on)
    - segment_states = [True, True, True, True, True, True, True]
    - if [True, True, True, True, True, True, True]: Do nothing, wait for segments to turn off
    - if segment_states[0] == True: can turn on segment_states 1 and/or 5
    - if segment_states[1] == True: can turn on segment_states 0 and/or 2 and/or 6
    - if segment_states[2] == True: can turn on segment_states 1 and/or 3 and/or 6
    - if segment_states[3] == True: can turn on segment_states 2 and/or 4
    - if segment_states[4] == True: can turn on segment_states 3 and/or 5 and/or 6
    - if segment_states[5] == True: can turn on segment_states 0 and/or 4 and/or 6
    - if segment_states[6] == True: can turn on segment_states 1 and/or 2 and/or 4 and/or 5
    - to reomve: get segment states and store:
      - 2 states ago = last_segment_state
      - last_segement_state = segement_states
      - if segment_state[i] == 2_states_ago[i] == True, then make segment_state[i] false
    - order of operations:
      - record last two segment states
      - calculate new segment states (add segments)
      - determine if segmenets need to be removed (remove segments)
      - draw new segment state

    

'''


import pygame
from pygame.constants import NUMEVENTS, WINDOWHITTEST
import colors
from time import sleep
from random import choice
from random import randint

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

seven_segment_coords_half = []
half_size_width = 75
half_size_height = 120

# Calculate coords for a half size seven segment display
for segment in seven_segment_coords:
    new_segment = []
    for coord in segment:
        new_coord = []
        new_coord.append(coord[0] / 2)
        new_coord.append(coord[1] / 2)
        new_segment.append(new_coord)
    new_segment
    seven_segment_coords_half.append(new_segment)
        
    

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

def draw_line_grid():
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
            coord = [seven_segment_coords_half[i][j][0] + xy[0], seven_segment_coords_half[i][j][1] + xy[1]]
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
 
def draw_segment_grid(rows, columns, segment_states):
    '''
    draws a grid of seven segment displays
    '''   
    for column in range(columns):
        for row in range(rows):
            draw_seven_segment(segment_states, colors.YELLOW, [half_size_width * column, half_size_height * row])  
            
def draw_segment_grid_random(rows, columns):
    '''
    draws a grid of seven segment displays
    '''   
    for column in range(columns):
        for row in range(rows):
            random_segments = randomize()
            draw_seven_segment(random_segments, colors.YELLOW, [half_size_width * column, half_size_height * row])       
        
def randomize():
    values = [choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False]),choice([True, False])]
    return values

def random_segment(num_segments = 1):
    # initialize segment values and create a list
    values = [False, False, False, False, False, False, False]
    segment_on = []
    
    for i in range(num_segments):
        # select which segement to turn on and add to a list
        segment_on.append(randint(0,6))
        
    for i in range(len(segment_on)):
        values[segment_on[i]] = True
        
    return values

def draw_rect_alpha(surface, color, rect):
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)

'''
- to reomve: get segment states and store:
    - 2 states ago = last_segment_state
    - last_segement_state = segement_states
    - if segment_state[i] == 2_states_ago[i] == True, then make segment_state[i] false
- order of operations:
    - record last two segment states
    - calculate new segment states (add segments)
    - determine if segmenets need to be removed (remove segments)
      - draw new segment state
    '''
    
def get_last_segment_states(segment_states,one_state_ago):
    two_states_ago = one_state_ago
    #print(f'two_states_ago: {two_states_ago}')
    one_state_ago = segment_states
    return([one_state_ago,two_states_ago])

def new_segments(segment_states):
    if segment_states[0] == True: 
        if segment_states[1] == False: segment_states[1] = choice([True, False])
        if segment_states[5] == False: segment_states[5] = choice([True, False])
    if segment_states[1] == True: 
        if segment_states[0] == False: segment_states[0] = choice([True, False])
        if segment_states[2] == False: segment_states[2] = choice([True, False])
        if segment_states[6] == False: segment_states[6] = choice([True, False])
    if segment_states[2] == True: 
        if segment_states[1] == False: segment_states[1] = choice([True, False])
        if segment_states[2] == False: segment_states[3] = choice([True, False])
        if segment_states[6] == False: segment_states[6] = choice([True, False])
    if segment_states[3] == True: 
        if segment_states[2] == False: segment_states[2] = choice([True, False])
        if segment_states[4] == False: segment_states[4] = choice([True, False])
    if segment_states[4] == True: 
        if segment_states[3] == False: segment_states[3] = choice([True, False])
        if segment_states[5] == False: segment_states[5] = choice([True, False])
        if segment_states[6] == False: segment_states[6] = choice([True, False])
    if segment_states[5] == True: 
        if segment_states[0] == False: segment_states[0] = choice([True, False])
        if segment_states[4] == False: segment_states[4] = choice([True, False])
        if segment_states[6] == False: segment_states[6] = choice([True, False])
    if segment_states[6] == True: 
        if segment_states[1] == False: segment_states[1] = choice([True, False])
        if segment_states[2] == False: segment_states[2] = choice([True, False])
        if segment_states[4] == False: segment_states[4] = choice([True, False])
        if segment_states[5] == False: segment_states[5] = choice([True, False])
    for i in range(len(segment_states)):
        if segment_states[i] == True:
            break
        else: 
            segment_states[randint(0,6)] = True
    return(segment_states)

def kill_segments(segment_states,last_segment_states):
    # If segment has been on for 2 cycles, turn it off
    for i in range(len(segment_states)):
        if segment_states[i] == last_segment_states[i] and segment_states[i] == True:
            segment_states[i] = False
            #print(f'segment {i} killed')
    return(segment_states)


# run at start of prgram
segment_states = randomize()
one_state_ago = []


    
################
# SETUP CONFIG #
################



while True:

    gameDisplay.fill(colors.BLACK)     # clear screen 
    
    # (r,g,b,a=0-255), (rect location)
    # draw_rect_alpha(gameDisplay, (0, 0, 0, 170), (0, 0, XRES, YRES))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()

    ''' Random Segments '''
    random_segments = randomize()
    draw_line_grid() 
    draw_segment_grid(5,12,random_segments)
    draw_segment_grid_random(5,12)
    
        
    ''' Drunk Random Segments '''    
    # if one_state_ago == []:
    #     one_state_ago = [False, False, False, False, False, False, False]
    # elif one_state_ago == [False, False, False, False, False, False, False]:
    #     segment_states = random_segment(2)
    # else: 
    #     one_state_ago = last_segment_states[0]  
    
    # last_segment_states = get_last_segment_states(segment_states, one_state_ago)    
    # segment_states = new_segments(segment_states)
    # segment_states = kill_segments(segment_states,last_segment_states[1]) # two states ago
   
   
    draw_segment_grid(5,12,segment_states)
    sleep(.3)
    pygame.display.update()
