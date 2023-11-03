import pygame as pg

## QUESTIONS // TODOS:
## - How can I edit other aspects of a text box using keys while the box is active?
## -- maybe two types of active mode? Text edit mode, box edit mode, and live mode?


pg.init()
screen = pg.display.set_mode((640, 480))
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
COLOR_HOVER = pg.Color('green')
FONT = pg.font.Font(None, 32)


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    print(self.text)
                    self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)



def main():
    clock = pg.time.Clock()
    #input_box1 = InputBox(100, 100, 140, 32) # initialize a text box
    #input_box2 = InputBox(100, 300, 140, 32)
    #input_boxes = [input_box1, input_box2]
    input_boxes = []
    done = False
    edit_mode = True

    # Main game loop:
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            for box in input_boxes:
                box.handle_event(event)
            if event.type == pg.MOUSEBUTTONDOWN:
                # if the mouse is colliding with an existing input box rect, or if there is a box that is active do nothing
                # else create a new input box rect
                x,y = event.pos # Or pg.mouse.get_pos()
                draw_new_input_box = True
                
                for box in input_boxes:
                    if box.rect.collidepoint(event.pos) or box.active:
                        draw_new_input_box = False
                        
                if draw_new_input_box == True:
                    new_input_box = InputBox(x, y, 140, 32)
                    input_boxes.append(new_input_box)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_BACKSPACE:        
                    # if text box empty, delete text box
                    # else delete the last character
                    for box in input_boxes:
                        if box.active and box.text == '':
                            input_boxes.remove(box)
                             

        for box in input_boxes:
            box.update()

        screen.fill((30, 30, 30))
        for box in input_boxes:
            box.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()