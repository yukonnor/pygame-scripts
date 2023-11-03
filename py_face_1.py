'''
Runs on Python 3.8.3 /anaconda/

Todo:
- make each section of face animatable / changeable relative to the others

'''


import pygame
from pygame.constants import WINDOWHITTEST
import colors
from time import sleep
import random

XRES = 800
YRES = 600
MIDPOINT_X = XRES / 2

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.BLACK)

reset_face = False

# face border global vars
border_top_left = [0,0]  # [x,y]
border_top_right = [0,0]
border_bottom_left = [0,0]
border_bottom_right = [0,0]

# face hair gloabl vars
hair_origin = [0,0]
hair_end = [0,0]
hair_distance = 10

# face eyes & brows global vars
left_brow_top_left = [0,0]
left_brow_top_right = [0,0]
left_brow_bottom_left = [0,0]
left_brow_bottom_right = [0,0]
right_brow_top_left = [0,0]
right_brow_top_right = [0,0]
right_brow_bottom_left = [0,0]
right_brow_bottom_right = [0,0]
eye_distance = 0
left_eye_center = [0,0]
right_eye_center = [0,0]
eye_radius = 10

# face nose global vars
nose_top = [0,0]
nose_corner = [0,0]
nose_edge = [0,0]

# face mouth global vars
mouth_left = [0,0]
mouth_right = [0,0]
mouth_mid_left = [0,0]
mouth_mid_right = [0,0]



# FACE BORDER
def new_top_left():
    x_min = 0 + 50
    x_max = MIDPOINT_X - 50  
    x = random.randint(x_min,x_max)
    y = 100
    a = [x,y]
    return a

def new_top_right():
    x = XRES - border_top_left[0]
    y = 100
    a = [x,y]
    return a

def new_bottom_left():
    x_min = 0 + 50
    x_max = (XRES/2) - 50 
    x = random.randint(x_min,x_max)
    y = 500
    a = [x,y]
    return a

def new_botom_right():
    x = (MIDPOINT_X - border_bottom_left[0]) + MIDPOINT_X
    y = 500
    a = [x,y]
    return a


def draw_border():
  
    pygame.draw.polygon(gameDisplay, colors.BLACK, (border_top_left, border_top_right, border_bottom_right, border_bottom_left), 0)  # fill face
    pygame.draw.polygon(gameDisplay, colors.WHITE, (border_top_left, border_top_right, border_bottom_right, border_bottom_left), 2)  # fill face


# FACE HAIR
def new_hair_origin():
    x = border_top_left[0]
    y = border_top_left[1]
    a = [x,y]
    return a

def new_hair_end():
    x_min = 0 + 100
    x_max = XRES - 100
    x = random.randint(x_min,x_max)
    y_min = 5 
    y_max = border_top_left[1] + 40
    y = random.randint(y_min, y_max )

    # recalculate y if too close to top of head
    if abs(border_top_left[1] - y) < 10:
        while abs(border_top_left[1] - y) < 10:
            y = random.randint(y_min, y_max )
    a = [x,y]
    return a

def new_hair_spread(hairs = 5):
    hair_distance = (border_top_right[0] - hair_origin[0]) / hairs
    return hair_distance


def draw_hair(hairs = 5): 
    
    for i in range(hairs + 1):
        pygame.draw.line(gameDisplay, colors.WHITE, (hair_origin[0] + (i * hair_distance), hair_origin[1]),(hair_end[0] + (i * hair_distance), hair_end[1]),1)


# FACE EYES
# Left eye coordinates are determined first
def new_left_brow_top_right():
    x_min = MIDPOINT_X - 100 
    x_max = MIDPOINT_X - 10 
    x = random.randint(x_min,x_max)
    y_min = border_top_left[1] + 10  # top
    y_max = (border_bottom_left[1] - border_top_left[1])/2 + border_top_left[1]  # bottom - midway down face
    y = random.randint(y_min,y_max)
    a = [x,y]

    #print(f"Eye top right X = {x}")
    return a

def new_left_brow_top_left():
    x = left_brow_top_right[0] - random.randint(10,40)
    y = left_brow_top_right[1]
    a = [x,y]
    return a

def new_eye_botom_right():
    # TODO: Eyebrow should be wider than it is tall
    x_min = MIDPOINT_X - 40 
    x_max = MIDPOINT_X - 10 
    x = random.randint(x_min,x_max)
    brow_width = left_brow_top_right[0] - left_brow_top_left[0]
    y_min = left_brow_top_left[1] + 10  # top
    y_max = max(y_min, left_brow_top_left[1] + brow_width)  # bottom 
    y = random.randint(y_min,y_max)
    a = [x,y]
    return a

def new_left_brow_bottom_left():
    x_min = max(border_top_left[0], border_bottom_left[0])
    x_max = (XRES/2) - 50 
    x = random.randint(x_min,x_max)
    y = left_brow_bottom_right[1]
    a = [x,y]
    return a

def new_right_brow_top_left():
    x = XRES - left_brow_top_right[0]
    y = left_brow_top_right[1]
    a = [x,y]
    return a

def new_right_brow_top_right():
    x = XRES - left_brow_top_left[0]
    y = left_brow_top_left[1]
    a = [x,y]
    return a

def new_right_brow_bottom_left():
    x = XRES - left_brow_bottom_right[0]
    y = left_brow_bottom_right[1]
    a = [x,y]
    return a

def new_right_brow_bottom_right():
    x = XRES - left_brow_bottom_left[0]
    y = left_brow_bottom_left[1]
    a = [x,y]
    return a


def new_left_eye_center():
    x = (left_brow_top_right[0] - left_brow_top_left[0])/2 + left_brow_top_left[0]
    y = (left_brow_bottom_right[1] - left_brow_top_right[1])/2 + left_brow_bottom_right[1]
    a = [x,y]
    return a

def new_right_eye_center():
    x = (right_brow_top_right[0] - right_brow_top_left[0])/2 + right_brow_top_left[0]
    y = (right_brow_bottom_right[1] - right_brow_top_right[1])/2 + right_brow_bottom_right[1]
    a = [x,y]
    return a


def new_eye_radius():
    midbrow_y = (left_brow_bottom_left[1] - left_brow_top_left[1])/2 + left_brow_top_left[1]  
    distance_to_midbrow = left_eye_center[1] - midbrow_y
    r_min = 10
    r_max = max(10, distance_to_midbrow)
    r = random.randint(r_min,r_max)
    return r


def draw_eyes(blink_eyes, eyes_open):

    if blink_eyes:
        # switch between drawing eyes and drawing horizontal lines (blinks) at random intervals
        if eyes_open:
            # draw left eye
            pygame.draw.circle(gameDisplay, colors.WHITE, left_eye_center, eye_radius, 2)
            pygame.draw.circle(gameDisplay, colors.WHITE, left_eye_center, max(eye_radius-10,2)) # pupil

            # draw right eye
            pygame.draw.circle(gameDisplay, colors.WHITE, right_eye_center, eye_radius, 2)
            pygame.draw.circle(gameDisplay, colors.WHITE, right_eye_center, max(eye_radius-10,2)) # pupil
        else:
            # draw horizontal lines:
            left_eye_left_point = [left_eye_center[0] - eye_radius, left_eye_center[1]]
            left_eye_right_point = [left_eye_center[0] + eye_radius, left_eye_center[1]]
            right_eye_left_point = [right_eye_center[0] - eye_radius, right_eye_center[1]]
            right_eye_right_point = [right_eye_center[0] + eye_radius, right_eye_center[1]]

            pygame.draw.line(gameDisplay, colors.WHITE, left_eye_left_point, left_eye_right_point, 2)
            pygame.draw.line(gameDisplay, colors.WHITE, right_eye_left_point, right_eye_right_point, 2)
    else:
        # draw eyes normally        
        pygame.draw.circle(gameDisplay, colors.WHITE, left_eye_center, eye_radius, 2)
        pygame.draw.circle(gameDisplay, colors.WHITE, left_eye_center, max(eye_radius-10,2)) 

        pygame.draw.circle(gameDisplay, colors.WHITE, right_eye_center, eye_radius, 2)
        pygame.draw.circle(gameDisplay, colors.WHITE, right_eye_center, max(eye_radius-10,2)) 


def draw_eye_brows(animate_eyebrows
, brow_position):
    if animate_eyebrows:
        if brow_position == 'Up':
            # draw eyebrows up slightly
            left_brow_top_left_new = [left_brow_top_left[0], left_brow_top_left[1] - 5]
            left_brow_top_right_new = [left_brow_top_right[0], left_brow_top_right[1] - 10]
            left_brow_bottom_left_new = [left_brow_bottom_left[0], left_brow_bottom_left[1]]
            left_brow_bottom_right_new = [left_brow_bottom_right[0], left_brow_bottom_right[1] - 10]
            right_brow_top_left_new = [right_brow_top_left[0], right_brow_top_left[1] - 10]
            right_brow_top_right_new = [right_brow_top_right[0], right_brow_top_right[1] - 5]
            right_brow_bottom_left_new = [right_brow_bottom_left[0], right_brow_bottom_left[1] - 10]
            right_brow_bottom_right_new = [right_brow_bottom_right[0], right_brow_bottom_right[1]]
            
            # draw left eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (left_brow_top_left_new, left_brow_top_right_new, left_brow_bottom_right_new, left_brow_bottom_left_new))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (left_brow_top_left_new, left_brow_top_right_new, left_brow_bottom_right_new, left_brow_bottom_left_new), 2)

            # draw right eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (right_brow_top_left_new, right_brow_top_right_new, right_brow_bottom_right_new, right_brow_bottom_left_new))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (right_brow_top_left_new, right_brow_top_right_new, right_brow_bottom_right_new, right_brow_bottom_left_new), 2)
        
        elif brow_position == 'Down':
            # draw eyebrows down slightly
            left_brow_top_left_new = [left_brow_top_left[0], left_brow_top_left[1]]
            left_brow_top_right_new = [left_brow_top_right[0], left_brow_top_right[1] + 5]
            left_brow_bottom_left_new = [left_brow_bottom_left[0], left_brow_bottom_left[1]]
            left_brow_bottom_right_new = [left_brow_bottom_right[0], left_brow_bottom_right[1] + 10]
            right_brow_top_left_new = [right_brow_top_left[0], right_brow_top_left[1] + 5]
            right_brow_top_right_new = [right_brow_top_right[0], right_brow_top_right[1]]
            right_brow_bottom_left_new = [right_brow_bottom_left[0], right_brow_bottom_left[1] + 10]
            right_brow_bottom_right_new = [right_brow_bottom_right[0], right_brow_bottom_right[1]]
            
            # draw left eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (left_brow_top_left_new, left_brow_top_right_new, left_brow_bottom_right_new, left_brow_bottom_left_new))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (left_brow_top_left_new, left_brow_top_right_new, left_brow_bottom_right_new, left_brow_bottom_left_new), 2)

            # draw right eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (right_brow_top_left_new, right_brow_top_right_new, right_brow_bottom_right_new, right_brow_bottom_left_new))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (right_brow_top_left_new, right_brow_top_right_new, right_brow_bottom_right_new, right_brow_bottom_left_new), 2)
        
        else:
            # draw eyebrows normally
            # draw left eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (left_brow_top_left, left_brow_top_right, left_brow_bottom_right, left_brow_bottom_left))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (left_brow_top_left, left_brow_top_right, left_brow_bottom_right, left_brow_bottom_left), 2)

            # draw right eyebrow
            pygame.draw.polygon(gameDisplay,colors.BLACK, (right_brow_top_left, right_brow_top_right, right_brow_bottom_right, right_brow_bottom_left))
            pygame.draw.polygon(gameDisplay,colors.WHITE, (right_brow_top_left, right_brow_top_right, right_brow_bottom_right, right_brow_bottom_left), 2)

    else: 
        # draw eyebrows normally
        pygame.draw.polygon(gameDisplay,colors.BLACK, (left_brow_top_left, left_brow_top_right, left_brow_bottom_right, left_brow_bottom_left))
        pygame.draw.polygon(gameDisplay,colors.WHITE, (left_brow_top_left, left_brow_top_right, left_brow_bottom_right, left_brow_bottom_left), 2)

        pygame.draw.polygon(gameDisplay,colors.BLACK, (right_brow_top_left, right_brow_top_right, right_brow_bottom_right, right_brow_bottom_left))
        pygame.draw.polygon(gameDisplay,colors.WHITE, (right_brow_top_left, right_brow_top_right, right_brow_bottom_right, right_brow_bottom_left), 2)



# FACE NOSE
def new_nose_top():
    x = MIDPOINT_X
    y = left_eye_center[1]  
    a = [x,y]
    return a

def new_nose_corner():
    x_min = int(nose_top[0] - 20)
    x_max = int(nose_top[0] - 2)
    x = random.randint(x_min,x_max)
    y_min = int(nose_top[1] + 8)
    y_max = int(nose_top[1] + 100)
    y = random.randint(y_min,y_max)
    a = [x,y]
    return a

def new_nose_edge():
    x_min = nose_top[0] + 2
    x_max = nose_top[0] + 20
    x = random.randint(x_min,x_max)
    y = nose_corner[1]
    a = [x,y]
    return a



def draw_nose():

    pygame.draw.line(gameDisplay, colors.WHITE, nose_top, nose_corner, 2)
    pygame.draw.line(gameDisplay, colors.WHITE, nose_corner, nose_edge, 2)


# FACE MOUTH
mouth_left = [0,0]
mouth_right = [0,0]
mouth_mid_left = [0,0]
mouth_mid_right = [0,0]

def new_mouth_left():
    x_min = border_bottom_left[0] + 10
    x_max = max(x_min, MIDPOINT_X - 100)
    x = random.randint(x_min,x_max)
    y_min = nose_corner[1] + 10          # high
    y_max = border_bottom_left[1] - 50   # low
    y = random.randint(y_min,y_max)
    a = [x,y]
    return a

def new_mouth_mid_left():
    x_min = mouth_left[0] + 10
    x_max = mouth_left[0] + 50
    x = random.randint(x_min,x_max)
    y_min = mouth_left[1] - 30     # high
    y_max = mouth_left[1] + 30   # low
    y = random.randint(y_min,y_max)
    a = [x,y]
    return a

def new_mouth_mid_right():
    # mouth right side is symetical accross x midpoint. 
    x = (MIDPOINT_X - mouth_mid_left[0]) + MIDPOINT_X
    y = mouth_mid_left[1]
    a = [x,y]
    return a

def new_mouth_right():
    x = (MIDPOINT_X - mouth_left[0]) + MIDPOINT_X
    y = mouth_left[1]
    a = [x,y]
    return a

def draw_mouth():
    pygame.draw.line(gameDisplay, colors.WHITE, mouth_left, mouth_mid_left, 2)
    pygame.draw.line(gameDisplay, colors.WHITE, mouth_mid_left, mouth_mid_right, 2)
    pygame.draw.line(gameDisplay, colors.WHITE, mouth_mid_right, mouth_right, 2)

###############
def draw_face():
    draw_border()
    draw_hair()
    draw_eyes(blink_eyes, eyes_open)
    draw_eye_brows(animate_eyebrows
, brow_position)
    draw_nose()
    draw_mouth()

################
# SETUP CONFIG #
################

face_set = 0 # face not set at beginning of loop
animate_hair = False

eye_loop_count = 0
blink_eyes = True
eyes_open = True
open_duration = 20
closed_duration = 2

brow_loop_count = 0
animate_eyebrows = True
brow_position = 'Default'  # 'Default', 'Up', or 'Down'
reg_position_duration = 30
brow_up_down_duration = 3


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
                reset_face = True
    


    if animate_eyebrows:

        if brow_position == 'Default':
            if brow_loop_count >= reg_position_duration:
                brow_loop_count = 0
                brow_position = random.choice(['Up'])  # removing down brow as it seemed too mean
        else:
            if brow_loop_count >= brow_up_down_duration:
                brow_loop_count = 0
                brow_position = 'Default'
                # reset how long eyes are opened for:
                reg_position_duration = random.randint(5,25)

    if blink_eyes:

        if eyes_open == True:
            if eye_loop_count >= open_duration:
                eye_loop_count = 0
                eyes_open = False
        elif eyes_open == False:
            if eye_loop_count >= closed_duration:
                eye_loop_count = 0
                eyes_open = True
                # reset how long eyes are opened for:
                open_duration = random.randint(5,25)

    if reset_face:
        # reset face border
        border_top_left = new_top_left()
        border_top_right = new_top_right()
        border_bottom_left = new_bottom_left()
        border_bottom_right = new_botom_right()

        # reset hairs
        hair_origin = new_hair_origin()
        hair_end = new_hair_end()
        hair_distance = new_hair_spread()

        # reset eyes
        left_brow_top_right = new_left_brow_top_right()
        left_brow_top_left = new_left_brow_top_left()
        left_brow_bottom_right = new_eye_botom_right()
        left_brow_bottom_left = new_left_brow_bottom_left()
        right_brow_top_left = new_right_brow_top_left()
        right_brow_top_right = new_right_brow_top_right()
        right_brow_bottom_left = new_right_brow_bottom_left()
        right_brow_bottom_right = new_right_brow_bottom_right()
        left_eye_center = new_left_eye_center()
        right_eye_center = new_right_eye_center()
        eye_radius = new_eye_radius() 
       
        # reset nose
        nose_top = new_nose_top()
        nose_corner = new_nose_corner()
        nose_edge = new_nose_edge()

        # reset mouth
        mouth_left = new_mouth_left()
        mouth_mid_left = new_mouth_mid_left()
        mouth_mid_right = new_mouth_mid_right()
        mouth_right = new_mouth_right()
        
        # don't reset face again until asked to
        reset_face = False
        face_set = 1   # notes that the face has been set at least once

    if animate_hair and face_set:
        hair_end[0] = hair_end[0] + random.randint(-5,5)
        hair_end[1] = hair_end[1] + random.randint(-5,5)

        
        min_x = int(max(5, ((border_top_right[0] - hair_origin[0]) / 5) - 20))
        max_x = int((border_top_right[0] - hair_origin[0]) / 5)
        hair_distance = random.randint(min_x, max_x)  
        

        
    draw_face()
    
    

    # print(f"top_left_y = {top_left_y}")


    sleep(.1)
    pygame.display.update()
    
    eye_loop_count += 1
    brow_loop_count += 1
