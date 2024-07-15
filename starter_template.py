import pygame
import math
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 600 #square board
CELL_SIZE = BOARD_SIZE/8

#initializing a 8*8 grid
board = [[None]*3,[None]*3,[None]*3]
game_status = 'live'

#keeps track of the colour of the player whose turn it is
player_token = 1 #cross plays first
player_token_symbol = {1 : 'cross', -1 : 'dot'}
player_token_color = {1 : 'White', -1 : 'Black'}


#start the working of pygame
pygame.init()
fps = 60

# heading on the screen
heading_font = pygame.font.Font(None,30)
heading_surface = heading_font.render('TIC TAC TOE', True,'Olive')
heading_rect = heading_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT - BOARD_SIZE)/4))

#define the game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
#change the name that appears on the pygame window
pygame.display.set_caption('Tic Tac Toe')
clock = pygame.time.Clock()


def initialize_game():
    """create the screen, the board and draw the lines"""
    # do not declare or initialize any image or button in thi space
    screen.fill('Grey')

    # draw the lines
    # pygame.draw.line(screen,color='Black',start_pos=(100 + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
    #                     end_pos=(100 + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5),
    #                     width=2)

def reset_game():
    global board, player_token, game_status

    initialize_game()

run = True
initialize_game()
while run:
    clock.tick(fps) #set the maximum frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_status == 'live':
                x,y = pygame.mouse.get_pos()

                if x < (SCREEN_WIDTH - BOARD_SIZE)/2 or x > (SCREEN_WIDTH + BOARD_SIZE)/2 or y < (SCREEN_HEIGHT - BOARD_SIZE)/2 or y > (SCREEN_HEIGHT + BOARD_SIZE)/2:
                    pass
                    # out of the board
                else:
                    pass
                    # in the board

    pygame.display.update()

    if game_status == 'over':
        time.sleep(2)
        reset_game()


pygame.quit()