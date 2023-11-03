'''
TODO:


'''

import pygame
import pygame.display        # so that we can use autocomplete on display
import pygame.draw           # so that we can use autocomplete on draw
from pygame.locals import *  # so that we can use variables defined here w/o calling pygames.locals.etc every time
from colors import *
import random

pygame.init()  

DEBUG = False

# determin speed of animation
FPS = 30                       
fpsClock = pygame.time.Clock() 

# screen size
XRES = 800 
YRES = 800 

COLUMNS = 10
ROWS = 20
CELL_WIDTH = 20
GRID_OFFSET_X = (XRES - (CELL_WIDTH * COLUMNS))/2
GRID_OFFSET_Y = (YRES - (CELL_WIDTH * ROWS))/2

FONT = pygame.font.SysFont("retrogaming", 16) 
FONT_BIG = pygame.font.SysFont("retrogaming", 24) 
FONT_HUGE = pygame.font.SysFont("retrogaming", 48) 

BOMB_COUNT = 20

screen = pygame.display.set_mode((XRES,YRES))         


class Cell():
    def __init__(self, pos):
        self.pos = pos  # (row num, col num)
        self.hidden = True
        self.bomb = False
        self.flagged = False
        self.nearby_bomb_count = 0
        self.first_clicked = False
        self.pixel_pos = self.get_pixel_pos(pos)  # the actual location of the tile (even in transit)
        self.rect = pygame.Rect(self.pixel_pos[0], self.pixel_pos[1], CELL_WIDTH, CELL_WIDTH)
        
    def get_pixel_pos(self, pos):
        # get the rect position based on the space the tile is in       
        x = (pos[1] * CELL_WIDTH) + GRID_OFFSET_X
        y = (pos[0] * CELL_WIDTH) + GRID_OFFSET_Y
       
        return x,y
    
    def check_cell(self):
        # When a cell is clicked, make it shown and check whether it's a bomb
        self.hidden = False
        if self.bomb:
            return 'bomb'
        else:
            return self.nearby_bomb_count
        
    def assign_nearby_bomb_count(self, grid):
        # check up,down,left,right (and 4 diagnal) neihboring cells to see if they have bombs
        nearby_bomb_count = 0
        directions = [-1,0,1] 
        
        #if DEBUG: print(f'Nearby bombs for cell: {self.pos}')
         
        for dir_x in directions: 
            for dir_y in directions:
                
                same_cell = False
                if dir_x == 0 and dir_y == 0: 
                    same_cell = True
                
                row_to_check = self.pos[0] + dir_y
                col_to_check = self.pos[1] + dir_x
                                
                # if cell to check is in bounds and is NOT the cell being checked:
                if row_to_check >= 0 and row_to_check < ROWS and col_to_check >= 0 and col_to_check < COLUMNS and same_cell == False:
                    # then check the cell. 
                    cell = grid[row_to_check][col_to_check]  # grid is [rows][columns]
                    
                    #if DEBUG: print(f'    Checking direction {[dir_x,dir_y]}, which is neighbor cell: {cell.pos}, is it a bomb? {cell.bomb}')
                    
                    #If it's a bomb and if it's not the current cell, increment nearby_bomb_count
                    if cell.bomb == True:
                        nearby_bomb_count += 1
                        
        self.nearby_bomb_count = nearby_bomb_count
    
    def show_cell(self, grid):
        bomb_revealed = False
        
        if self.hidden == True:
            self.hidden = False
            
            if self.nearby_bomb_count == 0 and self.bomb == False:
                if DEBUG: print(f"    Cell {cell.pos} had no nearby bombs and was not a bomb. Opening neighbors.")
                bomb_revealed = self.open_neighbors(grid)
            
            elif self.nearby_bomb_count > 0:
                if DEBUG: print(f"    Cell {cell.pos} had 1+ nearby bombs. Opening neighbors.")
                bomb_revealed = self.bomb
            
            # if a bomb
            elif self.bomb:
                bomb_revealed = self.bomb
        
        return bomb_revealed
            
    def open_neighbors(self, grid):
        # if the cell was clicked was a "0", you can show all of its neighbors by default
        directions = [-1,0,1] 
        bomb_revealed = False
        
        for dir_x in directions: 
            for dir_y in directions:
                
                row_to_open = self.pos[0] + dir_y
                col_to_open = self.pos[1] + dir_x
                                
                # if cell to open is in bounds
                if row_to_open >= 0 and row_to_open < ROWS and col_to_open >= 0 and col_to_open < COLUMNS:
                    # get the cell. 
                    cell = grid[row_to_open][col_to_open] 
                    
                    # if it's hidden and not flagged, open it
                    if cell.hidden == True and cell.flagged == False:
                        if DEBUG: print(f"  Opening cell {cell.pos} as it was hidden and not flagged.")
                        is_bomb = cell.show_cell(grid)
                        if DEBUG: print(f"  Cell {cell.pos} a bomb? {is_bomb}")
                        if is_bomb:
                            bomb_revealed = True
                    
                    # if cell is hidden and flagged:    
                    elif cell.hidden == True and cell.flagged == True:
                        if DEBUG: print(f"  Keeping cell {cell.pos} closed it was flagged.")

                    
                    # if cell is shown
                    '''
                    else:
                        if DEBUG: print("Nothing to open.")
                        return self.bomb
                    '''
        return bomb_revealed
    
    def flag_cell(self):
        if self.flagged == False:
            self.flagged = True
        else: 
            self.flagged = False
            
    def flagged_open_shortcut(self, grid):
        # if a open cell is clicked and its nearby count == count of nearby flags, open neighbor closed cells
        nearby_flag_count = 0
        directions = [-1,0,1] 
        
        # get count of nearby flags
        for dir_x in directions: 
            for dir_y in directions:
                
                row_to_open = self.pos[0] + dir_y
                col_to_open = self.pos[1] + dir_x
                                
                # if cell to open is in bounds and is closed:
                if row_to_open >= 0 and row_to_open < ROWS and col_to_open >= 0 and col_to_open < COLUMNS:
                    # get the cell. 
                    cell = grid[row_to_open][col_to_open] 
                    
                    if cell.flagged == True:
                        nearby_flag_count += 1
        
        if nearby_flag_count > 0 and nearby_flag_count == self.nearby_bomb_count:
            if DEBUG: print(f"Using shortcut to open neighbors of cell {self.pos}.")
            is_bomb = self.open_neighbors(grid)
            if is_bomb:
                return is_bomb     
        else:
            if DEBUG: print("Shortcut cannot be used. Returning the bomb value of the cell that was clicked.")   
            return self.bomb

def create_grid():
    # add cells to the grid
    grid = []
    
    for r in range(ROWS):
        grid.append([]) # add an empty row
        for c in range(COLUMNS):
            new_cell = Cell((r,c))  # create a new cell at current row (y), column (x) position
            grid[r].append(new_cell) 
            
    return grid

def assign_bombs(grid): 

    # create a temp list for bombs
    bombs = []
    bombs_left = BOMB_COUNT
    bomb_placement_finalized = False

    for i in range(ROWS*COLUMNS):
        if bombs_left > 0:
            bombs.append(1)
        else:
            bombs.append(0)
        bombs_left -= 1
        
    while bomb_placement_finalized == False:
            
        # shuffle the bomb list
        random.shuffle(bombs)
        
        # increment through the grid to add the shuffled bombs
        for r,row in enumerate(grid):          
            for c,cell in enumerate(grid[r]):
                bomb_index = (r * COLUMNS) + c  
                
                if bombs[bomb_index] == 1: 
                    if cell.first_clicked == True:
                        # go back to the top of the loop to reshuffle bomb list and try again 
                        continue
                    else:
                        cell.bomb = True  
        
        # if successfully made it through bomb assignment: 
        bomb_placement_finalized = True 
        
def assign_nearby_bomb_count(grid):
    
    # increment through the grid to assign nearby bomb count to each cell
    for r,row in enumerate(grid):          
        for c,cell in enumerate(grid[r]): 
            cell.assign_nearby_bomb_count(grid)
            
def reveal_all(grid):
    
    # increment through the grid to reveal all cells
    for r,row in enumerate(grid):          
        for c,cell in enumerate(grid[r]): 
            cell.hidden = False

def first_click_actions(grid, first_clicked_cell):
    
    first_clicked_cell.first_clicked = True
    
    # Assign bomb values to cells, omitting the cell that was clicked
    assign_bombs(grid)
    
    # Assign neighbor values to cells    
    assign_nearby_bomb_count(grid)
    
    first_clicked_cell.show_cell(grid)    

def draw_grid(grid):
    
    for row_num, row_contents in enumerate(grid):
        for col_num, cell in enumerate(grid[row_num]):

            # if cell is hidden, draw a hidden square
            if cell.hidden:
                pygame.draw.rect(screen, GRAY, cell.rect)
                pygame.draw.rect(screen, BLACK, cell.rect, 1)
                if cell.flagged: 
                    text_surface = FONT.render("F", True, RED_ORANGE)
                    screen.blit(text_surface, (cell.rect.left + 4, cell.rect.top))
                    
            
            else:
                # if a bomb, draw a red square
                if cell.bomb:
                    pygame.draw.rect(screen, RED, cell.rect)
                    pygame.draw.circle(screen, BLACK, (cell.rect.centerx, cell.rect.centery), cell.rect.width/4 )
                    pygame.draw.rect(screen, BLACK, cell.rect, 1)
                
                # if not a bomb, draw nearyby_bomb count
                else:
                    pygame.draw.rect(screen, DARK_GRAY, cell.rect)
                    pygame.draw.rect(screen, BLACK, cell.rect, 1)
                    
                    # draw text for cell.nearby_bomb_count if > 0
                    if cell.nearby_bomb_count > 0: 
                        text_surface = FONT.render(str(cell.nearby_bomb_count), True, GREEN)
                        screen.blit(text_surface, (cell.rect.left + 4, cell.rect.top))

def draw_game_info(bombs_left): # add Time here later
    #
    text_surface = FONT_BIG.render(f"BOMBS LEFT: {bombs_left}", True, GREEN)
    
    # draw halfway between top of window and top row of cells 
    screen.blit(text_surface, (GRID_OFFSET_X, GRID_OFFSET_Y/2))

def draw_new_game_button():
    
    text_surface = FONT_BIG.render(f"< NEW GAME >", True, BLUE)
    text_rect = text_surface.get_rect()
    
    text_rect.centerx = XRES/2
    text_rect.centery = YRES - GRID_OFFSET_Y/2
    
    button_rect = pygame.Rect(text_rect)
    button_rect.width = text_rect.width + 10
    button_rect.height = text_rect.height + 10
    button_rect.centerx = XRES/2
    button_rect.centery = YRES - GRID_OFFSET_Y/2
    
    pygame.draw.rect(screen, GRAY, button_rect, border_radius=5)
    pygame.draw.rect(screen, DARK_GRAY, button_rect, 2, 5)
    screen.blit(text_surface, text_rect)
    
    return button_rect
    
def check_if_won(grid):
    # if all unflagged cells are open, game is won
    target = (ROWS * COLUMNS) - BOMB_COUNT
    cells_opened = 0
    
    for row_num, row_contents in enumerate(grid):
        for col_num, cell in enumerate(grid[row_num]):
            # if cell not a flag and is open, add to cells opened
            if cell.flagged == False and cell.hidden == False:
                cells_opened += 1
    
    if target - cells_opened == 0:
        # game won:
        return True
    
    else:
        return False
                
    
    
    
########################################
# GAME STARTUP
########################################
bombs_left = BOMB_COUNT
first_click = True
bombs_assigned = False
game_won = False
game_over = False
new_game = False

# Create grid
grid = create_grid()
 
# Draw grid & button
screen.fill(BLACK) 
draw_grid(grid)

new_game_button_rect = draw_new_game_button()
pygame.display.update()


               
        
########################################
# Main Game Loop
########################################
while True:
    screen.fill(BLACK)     # clear screen 
    
    # events & quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                quit()
            if event.key == pygame.K_r:
                reveal_all(grid)
            if event.key == pygame.K_n:
                new_game = True
                
        # if LEFT MOUSE button clicked (TODO instead change to released: MOUSEBUTTONUP)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            pos = pygame.mouse.get_pos()
            is_bomb = False
            
            # check if cursor is on a cell
            for r,row in enumerate(grid):
                for cell in grid[r]:
                    if cell.rect.collidepoint(pos) and cell.flagged == False:
                        # tell the game that a cell has been clicked to kick things off
                        
                        if first_click == True: 
                            # Run first click actions:
                            first_click_actions(grid, cell)
                            first_click = False
                            
                        # if it's already open AND if the nearby count == nearby flags, open the neighboring cells 
                        if cell.hidden == False:
                            is_bomb = cell.flagged_open_shortcut(grid)
                            if DEBUG: print(f"Flag Open Shortcut: Is bomb? {is_bomb}")
                            
                            if is_bomb:
                                game_over = True
                                if DEBUG: print("GAME OVER!")
                            
                        # if cell is closed, show the cell content
                        if cell.hidden == True:
                            is_bomb = cell.show_cell(grid) 
                            if DEBUG: print(f"Show Cell: Is bomb? {is_bomb}")
                            
                            # if a cell was opened that is a bomb, end the game
                            if is_bomb:
                                game_over = True
                                if DEBUG: print("GAME OVER!")
            
            # check if cursor is on the new game button           
            if new_game_button_rect.collidepoint(pos):
                new_game = True         
                                 
                        
        # if RIGHT MOUSE button clicked, flag a closed cell
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            # if a cell is clicked:
            pos = pygame.mouse.get_pos()
            # check if cursor is on a cell
            for r,row in enumerate(grid):
                for cell in grid[r]:
                    if cell.rect.collidepoint(pos) and cell.hidden == True:
                        # add or remove flag to the cell 
                        cell.flag_cell()
            
                        # decrement bombs left 
                        bombs_left -= 1                            
       
    draw_grid(grid)
    draw_game_info(bombs_left)
    draw_new_game_button()
    
    if bombs_left == 0: 
        game_won = check_if_won(grid)
    
    if game_over:
        
        reveal_all(grid)
        
        text_surface_top = FONT_HUGE.render(f"GAME OVER", True, RED)
        top_text_rect = text_surface_top.get_rect()
        top_text_rect.center = (XRES/2, YRES/2)
        
        text_surface_bottom = FONT_HUGE.render(f"GAME OVER", True, BLACK)
        bot_text_rect = text_surface_bottom.get_rect()
        bot_text_rect.center = (XRES/2, YRES/2 + 5)
    
        # draw halfway between top of window and top row of cells 
        screen.blit(text_surface_bottom, bot_text_rect)
        screen.blit(text_surface_top, top_text_rect)
        
    if game_won:
        
        text_surface_top = FONT_HUGE.render(f"YOU WIN!", True, GREEN)
        top_text_rect = text_surface_top.get_rect()
        top_text_rect.center = (XRES/2, YRES/2)
        
        text_surface_bottom = FONT_HUGE.render(f"YOU WIN", True, BLACK)
        bot_text_rect = text_surface_bottom.get_rect()
        bot_text_rect.center = (XRES/2, YRES/2 + 5)
    
        # draw halfway between top of window and top row of cells 
        screen.blit(text_surface_bottom, bot_text_rect)
        screen.blit(text_surface_top, top_text_rect)
    
    if new_game: 
       
        # reset the counts
        bombs_left = BOMB_COUNT
        first_click = True
        bombs_assigned = False
        game_won = False
        game_over = False
        new_game = False

        # Rereate grid
        grid = create_grid()
        
        new_game = False
        
        
    pygame.display.update()
    fpsClock.tick(FPS)