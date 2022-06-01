
import pygame
import os
from os import system
from random import randint

from pyparsing import White

CURRENT_DIR = os.path.dirname(__file__)
os.chdir(CURRENT_DIR)

system("cls")
pygame.init()

scale = 75

display_x, display_y = 16*scale, 9*scale

background_color = [0, 0, 0]
grey = (38, 38, 38)
green = (50, 150, 75)
orange = (225, 200, 50)
red = (255, 50, 0)

background = pygame.display.set_mode((display_x,display_y))
pygame.display.set_icon(pygame.image.load("icon.png"))

cell_size = scale*4//3
letter_size = int(cell_size//1.5)


# ========================================= Classes ========================================= #
class Grid:

    def __init__(self, x, y, i, j, thickness, cell_size, color = "white"):
        
        self.x, self.y, self.i, self.j, self.thickness, self.cell_size, self.color = x, y, i, j, thickness, cell_size, color
        self.draw_x, self.draw_y = self.x - (self.cell_size*self.i //2), self.y - (self.cell_size*self.j //2)
        self.coordinates = []

        for i in range(self.j):
            row = i*self.cell_size + self.thickness
            for j in range(self.i):
                self.coordinates.append((self.draw_x+j*self.cell_size+self.thickness, self.draw_y + row))
    
    def draw(self):


        for i in range(self.i + 1):
            draw_rect(self.draw_x + i*self.cell_size, self.draw_y, self.thickness, self.j*self.cell_size + self.thickness, self.color)

        for j in range(self.j + 1):
            draw_rect(self.draw_x, self.draw_y + j*self.cell_size, self.i*self.cell_size + self.thickness, self.thickness, self.color)

    def fill_cell(self, number, color):

        x, y = self.coordinates[number][0], self.coordinates[number][1]
        draw_rect(x, y, self.cell_size - self.thickness, self.cell_size - self.thickness, color)

    def place_letter(self, number, letter, bg_color = background_color):

        x, y = self.coordinates[number][0], self.coordinates[number][1]
        display_text(x + self.cell_size//2 - self.thickness//2, y + self.cell_size//2 + self.thickness//2, letter, int(self.cell_size//1.5), 'white', bg_color)
# ========================================= Functions ========================================= #

def draw_rect(x, y , width, height, color):
    
    pygame.draw.rect(background, color, (x, y, width, height))

def display_text(x, y, text, size, color, bg_color, center = True):

    if center:
        font = pygame.font.Font("freesansbold.ttf", size)
        text_render = font.render(text, True, color, bg_color)
        background.blit(text_render, text_render.get_rect(center = (x, y)))
    
    else:
        font = pygame.font.Font('freesansbold.ttf', size)
        background.blit(font.render(text, True, color, bg_color), [x, y])

def place_button(x, y, text, text_size, text_color, color, border_thickness, border_color):

    border_width = len(text)*text_size//1.8
    border_height = text_size*1.5

    draw_rect(x - border_width//2, y - border_height//2, border_width + border_thickness, border_height + + border_thickness, border_color)
    draw_rect(x - border_width//2 + border_thickness, y - border_height//2+border_thickness, border_width - border_thickness, border_height - border_thickness, color)

    display_text(x, y, text, text_size, text_color, color)

def is_valid(key_name):

    if not key_name.isalpha() or len(key_name)>1 : return False
    return True

def receivable():

    if len(input_array)==5 or len(letter_array)==25 : return False
    return True

def get_input():

    key = pygame.key.name(event.key).upper()

    if not is_valid(key) or not receivable() : return

    letter_array.append(key)
    input_array.append(key)
    map_letters()

def map_letters():

    for number in range(len(input_array)):

        main_grid.place_letter(5*input_amount + number, input_array[number])

def generate_word():

    return words_array[randint(0, len(words_array)-1)]

def display_message(message):

    pass

def reset_right_side():

    draw_rect(display_y + 3, 0, display_x - display_y, display_y, background_color)

def reset_main_grid():

    for number in range(25):
        main_grid.fill_cell(number, background_color)

def restart_game():

    global input_amount
    global word

    input_amount = 0
    word = generate_word()

    letter_array.clear()
    input_array.clear()
    reset_main_grid()

    show_tutorial()

def color_line():

    for i in range(5):

        if input_array[i]==word[i]:
            main_grid.fill_cell(5*input_amount + i, green)
            main_grid.place_letter(5*input_amount + i, input_array[i], green)

        elif input_array[i] in word:
            main_grid.fill_cell(5*input_amount + i, orange)
            main_grid.place_letter(5*input_amount + i, input_array[i], orange)

        else:
            main_grid.fill_cell(5*input_amount + i, grey)
            main_grid.place_letter(5*input_amount + i, input_array[i], grey)

def win_event():

    hide_tutorial()
    display_text(display_y + (display_x-display_y)//2, display_y//2 - scale*1.1, "YOU WON!", letter_size, "white", background_color, True)

    line_spacing = 3

    end = "tries"
    if input_amount==0:
        end = "try"
    display_text(display_y + (display_x-display_y)//2 , scale*line_spacing*1.5, f"You guessed the word in {input_amount+1} {end}!", int(letter_size//3.5), green, background_color)


def lose_event():

    reset_main_grid()
    for number in range(25):
        main_grid.fill_cell(number, red)
        main_grid.place_letter(number, word[number%5], red)

    hide_tutorial()
    display_text(display_y + (display_x-display_y)//2, display_y//2 - scale*1.1, "YOU LOST!", letter_size, "white", background_color, True)

    line_spacing = 3

    display_text(display_y + (display_x-display_y)//2 , scale*line_spacing*1.5, f"The word was {word}.", int(letter_size//3.5), red, background_color)
    display_text(display_y + (display_x-display_y)//2 , scale*line_spacing*2, "Press (ESC) or (Space) key to play again.", int(letter_size//3.5), "white", background_color)




def draw_separator():

    draw_rect(display_y - 2, 0, 5, display_y, grey)
    




def show_tutorial():

    global tutorial_in_view
    tutorial_in_view = True

    reset_right_side()

    display_text(display_y + (display_x-display_y)//2, scale//1.5, "HOW TO PLAY", letter_size//2, 'white', background_color)

    line_spacing = 1.2
    for sentence in sentences_section1:

        if not sentence.endswith(('.', ':', '!')):
            display_text(display_y + scale//4 , scale*line_spacing, sentence, int(letter_size//3.5), 'white', background_color, False)
            line_spacing+=0.3
        else:
            display_text(display_y + scale//4 , scale*line_spacing, sentence, int(letter_size//3.5), 'white', background_color, False)
            line_spacing+=0.5

    tutroial_grid = Grid(display_y + cell_size*.75*2.5 + scale//4, line_spacing*scale + cell_size*.75//2, 5, 1, 3, cell_size*.75)
    tutroial_grid.draw()
    tutroial_grid.fill_cell(0, green)
    tutroial_grid.fill_cell(1, grey)
    tutroial_grid.fill_cell(2, grey)
    tutroial_grid.fill_cell(3, orange)
    tutroial_grid.fill_cell(4, grey)
    tutroial_grid.place_letter(0, 'O', green)
    tutroial_grid.place_letter(1, 'T', grey)
    tutroial_grid.place_letter(2, 'H', grey)
    tutroial_grid.place_letter(3, 'E', orange)
    tutroial_grid.place_letter(4, 'R', grey)

    line_spacing += tutroial_grid.cell_size//scale + .5
    for sentence in sentences_section2:

        if not sentence.endswith(('.', ':', '!')):
            display_text(display_y + scale//4 , scale*line_spacing, sentence, int(letter_size//3.5), 'white', background_color, False)
            line_spacing+=0.3
        else:
            display_text(display_y + scale//4 , scale*line_spacing, sentence, int(letter_size//3.5), 'white', background_color, False)
            line_spacing+=0.5
    
    line_spacing += 0.5

def hide_tutorial():

    global tutorial_in_view
    tutorial_in_view = False

    reset_right_side()


    

# ========================================= Keybinds ========================================= #
def escape_event():

    global close_window

    if len(letter_array)!=0:
        restart_game()
    else:
        close_window = True

def enter_event():

    global input_amount
    if input_amount==5:
        return

    if len(input_array)!=5 : return

    if ''.join(input_array) not in words_array:

        # display_message("Not in word list!")
        return

    color_line()

    if ''.join(input_array)==word:
        win_event()
        return

    if input_amount==4:
        lose_event()
        input_amount+=1
        return

    input_array.clear()
    input_amount+=1

def backspace_event():

    if len(input_array)==0 : return

    if ''.join(input_array)==word or input_amount==5: return

    letter_array.pop()
    input_array.pop()
    
    main_grid.fill_cell(len(input_array) + 5*input_amount, background_color)


def space_event():

    pass



    






# ========================================= Characters ======================================== #

letter_array = []
input_array = []
input_amount = 0

with open("words.txt", 'r') as words_file:

    words_array = [word[:-1] for word in words_file.readlines()]

word = generate_word()

tutorial_in_view = True



# ========================================= Instances ========================================= #
main_grid = Grid(display_y//2, display_y//2, 5, 5, 4, cell_size)
sentences_section1 = ["Guess the word in five tries.", "Each guess must be a valid five-letter word.", "Hit the enter button to submit.", "After each guess, the color of tiles will change in the", "following manner:"]
sentences_section2 = ["The letter O is in the correct spot.", "The letter E is in the word, but not the correct spot.", "The rest of the letters are not in the word.", "Good luck!"]



# ========================================= Main Game ========================================= #
close_window = False
background.fill(background_color)

main_grid.draw()
draw_separator()
show_tutorial()


while not close_window:
    
    PING = 50
    pygame.display.set_caption("Wordle: Guess The Word")
    pygame.time.delay(PING)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            close_window = True

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                escape_event()
            
            if event.key == pygame.K_RETURN:
                enter_event()
            
            if event.key == pygame.K_BACKSPACE:
                backspace_event()
            
            if event.key == pygame.K_SPACE:
                space_event()
            
            get_input()


# ============================================================================================ #
    pygame.display.update()