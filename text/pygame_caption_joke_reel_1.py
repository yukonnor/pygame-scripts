import pygame as pg

## TODOS:
## - 1st scene: "A Few Jokes" Title
## - 2nd scene: "Joke 1". Delay 10s. At 5s show timer
## - 3rd scene: "Joke 1" + "Answer 1". Delay 5s
## - 4th scene: "Next joke in 5,4,3,2,1"


pg.init()
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
TEXT_COLOR= pg.Color("white")
COLOR_ACTIVE = pg.Color("dodgerblue2")
COLOR_HOVER = pg.Color("green")
FONT = pg.font.SysFont("retrogaming", 24) 
FONT_SMALL = pg.font.SysFont("retrogaming", 20) 

INTRO_DURATION = 2
QUESTION_DURATION = 5
Q_AND_ANSWER_DURATION = QUESTION_DURATION + 5
NEXT_JOKE_DURATION = Q_AND_ANSWER_DURATION + 5
END_DURATION = 5

intro_text = "A FEW JOKES..."
seconds_left = 5
next_joke_text = f"NEXT JOKE IN...{seconds_left}"
answer_revealed_countdown = f"{seconds_left}"
jokes = ["I BOUGHT SOME SHOES FROM A DRUG DEALER",
         "HOW DOES NASA ORGANIZE A PARTY?",
         "A FRIEND TOLD ME THEY'RE DOING YOGA EVERYDAY NOW",]
answers = ["I DON'T KNOW WHAT HE LACED THEM WITH BUT I CAN'T STOP TRIPPING",
           "THEY PLANET",
           "IT'S A BIT OF A STRETCH"] 
end_text = "HA HA HA  THANK YOU  HA HA HA"


def show_seconds(seconds):
    seconds_text = f"{seconds}"
    text_surface = FONT.render(seconds_text, True, TEXT_COLOR)
    screen.blit(text_surface, (550, 400))
    
def draw_multiline_text(surface, text, pos, font, color):
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            text_surface = font.render(word, 0, color)
            word_width, word_height = text_surface.get_size()
            if x + word_width >= max_width - 30:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(text_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.

def draw_centered_text(surface, text, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
    surface.blit(text_surface, text_rect)

def main():
    clock = pg.time.Clock()
    start_ticks = pg.time.get_ticks()
    #input_box1 = InputBox(100, 100, 140, 32) # initialize a text box
    #input_box2 = InputBox(100, 300, 140, 32)
    #input_boxes = [input_box1, input_box2]
    input_boxes = []
    done = False
    joke_counter = 0 
    scene = "Intro"

    # Main game loop:
    while not done:
        seconds = int((pg.time.get_ticks() - start_ticks)/1000) #calculate how many seconds have passed
        
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True     
                                     
        screen.fill((0, 0, 0))
        
        if scene == "Intro":
            if seconds < INTRO_DURATION:
                # show intro text statically
                draw_centered_text(screen, intro_text, FONT, TEXT_COLOR)                
                show_seconds(seconds)
                
            elif seconds < 4:
                # TODO flash intro text
                pass
            else:
                # move to jokes and reset timer
                scene = "Jokes"
                start_ticks = pg.time.get_ticks()
            
        if scene == "Jokes":            
            if joke_counter > len(jokes) - 1:
                # move to end scene and reset timer
                scene = "End"
                start_ticks = pg.time.get_ticks()
            else:
                seconds = int((pg.time.get_ticks() - start_ticks)/1000)
                if seconds < QUESTION_DURATION:
                    # show joke
                    draw_multiline_text(screen, jokes[joke_counter], (50,100), FONT_SMALL, TEXT_COLOR)
                    
                    show_seconds(seconds)
                    
                elif seconds < Q_AND_ANSWER_DURATION:
                    # show joke
                    draw_multiline_text(screen, jokes[joke_counter], (50,100), FONT_SMALL, TEXT_COLOR)
                    # show answer
                    draw_multiline_text(screen, answers[joke_counter], (50,200), FONT_SMALL, TEXT_COLOR)
                    
                    show_seconds(seconds)
                    #print("Joke and answer text")
                    
                elif seconds < NEXT_JOKE_DURATION and joke_counter < len(jokes) - 1: # only show if there are more jokes
                    # show "next joke in" text
                    seconds_left = NEXT_JOKE_DURATION - seconds
                    next_joke_text = f"NEXT JOKE IN...{seconds_left}"
                    draw_centered_text(screen, next_joke_text, FONT, TEXT_COLOR)
                    
                    show_seconds(seconds)
                    #print("Next joke text")
                    
                else:
                    # move to the next joke. reset counter and timer.
                    joke_counter += 1
                    start_ticks = pg.time.get_ticks()                
                
        if scene == "End":
            if seconds < 1000:
                # show end text
                draw_centered_text(screen, end_text, FONT, TEXT_COLOR)
                show_seconds(seconds)
            else:
                # program done
                pass # stay on black screen
                #done = True

        pg.display.flip()
        clock.tick(2)  # was 30. Now will only show 2 FPS 


if __name__ == "__main__":
    main()
    pg.quit()
    
    
    
    
    
'''
# check to see if joke question text is long
if len(jokes[joke_counter]) > 33:
    # if long, break into multiple lines
    n = 33
    substrings = [jokes[joke_counter][i:i+n] for i in range(0, len(jokes[joke_counter]), n)]
    y_position = 100
    for line in substrings:
        text_surface = FONT_SMALL.render(line, True, TEXT_COLOR)
        screen.blit(text_surface, (50, y_position))
        y_position += 25
else:
    # else, just print the line
    text_surface = FONT_SMALL.render(jokes[joke_counter], True, TEXT_COLOR)
    screen.blit(text_surface, (50, 100))
'''