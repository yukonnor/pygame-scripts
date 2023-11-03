import pygame
import colors
from time import sleep
import random

XRES = 800
YRES = 600

gameDisplay = pygame.display.set_mode((XRES,YRES))
gameDisplay.fill(colors.BLACK)

radius = 20
diameter = 2 * radius
num_rows = int(YRES / diameter) # overlapping

circ_y = []
circ_x = []

for i in range(num_rows):
    circ_x.append(random.randint(0,XRES))
    circ_y.append(i*2*radius + radius) 
    

dir = [] # 1 for moving to right, -1 for moving to left
amount = []
sleep_cycles = 200
sleep_count = []
update_destination = []
destination = []

for i in range(num_rows):
    update_destination.append(True)
    destination.append(0)
    sleep_count.append(0)
    dir.append(random.choice([-1,1]))
    amount.append(random.randint(100,175))

def new_destination(i, direction, amount):
    new_destination = circ_x[i] + (direction * amount[i])
    return new_destination
    



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

    # DRAW SHAPES

    for i in range(num_rows):
        # draw lines
        # as circles get closer together, draw line brighter
        if i < num_rows-1:
            color_value = max(0, 255 - (abs(circ_x[i] - circ_x[i+1]))/1.5)
            line_color = (color_value, color_value, color_value)
            pygame.draw.line(gameDisplay, line_color, (circ_x[i],circ_y[i]),(circ_x[i+1],circ_y[i+1]),1)
        if i < num_rows-2:
            color_value = max(0, 255 - (abs(circ_x[i] - circ_x[i+2]))/1.5)
            line_color = (color_value, color_value, color_value)
            pygame.draw.line(gameDisplay, line_color, (circ_x[i],circ_y[i]),(circ_x[i+2],circ_y[i+2]),2)
        if i < num_rows-3:
            color_value = max(0, 255 - (abs(circ_x[i] - circ_x[i+3]))/1.5)
            line_color = (color_value, color_value, color_value)
            pygame.draw.line(gameDisplay, line_color, (circ_x[i],circ_y[i]),(circ_x[i+3],circ_y[i+3]),3)
        pygame.draw.circle(gameDisplay, colors.WHITE, (circ_x[i],circ_y[i]), radius)

        # draw circles

        #pygame.draw.circle(gameDisplay, colors.WHITE, (circ_x[i],circ_y[i]), radius) # white circles

        pygame.draw.circle(gameDisplay, colors.BLACK, (circ_x[i],circ_y[i]), radius)
        pygame.draw.circle(gameDisplay, colors.WHITE, (circ_x[i],circ_y[i]), radius, 2)

        
    
    # SET DESTINATIONS
    for i in range(num_rows):
        if update_destination[i]:
            destination[i] = new_destination(i, dir[i], amount)
            update_destination[i] = False
            #print(f"NEW DESTINATION! Destination = {destination[i]} and Direction = {dir[i]}")

        # if circle x hasn't reach it's destination, move towards it
        if dir[i] == 1:
            if circ_x[i] <= destination[i]:
                circ_x[i] += dir[i] * 1  
            # once it has reached its destination, 'pause' for x cycles
            elif circ_x[i] > destination[i]: 
                #circ_x[i] += 1
                sleep_count[i] += 1
                if sleep_count[i] >= sleep_cycles:
                    update_destination[i] = True
                    sleep_count[i] = 0
        elif dir[i] == -1:
            if circ_x[i] >= destination[i]:
                circ_x[i] += dir[i] * 1  
            # once it has reached its destination, 'pause' for x cycles
            elif circ_x[i] < destination[i]: 
                #circ_x[i] += 1
                sleep_count[i] += 1
                if sleep_count[i] >= sleep_cycles:
                    update_destination[i] = True
                    sleep_count[i] = 0
    

    # WRAP AROUND 
    for i in range(num_rows):
        if (circ_x[i] > (XRES + radius)) and dir[i] == 1:
            circ_x[i] = random.randint((-1 * amount[i]), (0 - radius))
            update_destination[i] = True
        if (circ_x[i] < (0 - radius)) and dir[i] == -1:
            circ_x[i] = random.randint((XRES + radius), XRES + amount[i])
            update_destination[i] = True
    #sleep(.1)
    pygame.display.update()
