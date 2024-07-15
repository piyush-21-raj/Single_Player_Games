import pygame
import math
import time

#variables defining the board and screen sizes
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
BOARD_SIZE = 300 #sqaure board

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

# initializing the X button
x_image = pygame.image.load('Graphics/x_image.png').convert_alpha()
x_image = pygame.transform.scale(x_image, (BOARD_SIZE/3, BOARD_SIZE/3))

# initializing the O button
o_image = pygame.image.load('Graphics/o_image.png').convert_alpha()
o_image = pygame.transform.scale(o_image, (BOARD_SIZE/3, BOARD_SIZE/3))


def initialize_game():
    """create the screen, the board and draw the lines"""
    # do not declare or initialize any image or button in thi space
    screen.fill('Grey')

    # game board
    board_image = pygame.image.load('Graphics/board.jpg').convert()
    board_image = pygame.transform.scale(board_image, (BOARD_SIZE, BOARD_SIZE))

    # paste the board onto the screen
    screen.blit(board_image,((SCREEN_WIDTH - BOARD_SIZE)/2,(SCREEN_HEIGHT - BOARD_SIZE)/2))
    screen.blit(heading_surface,heading_rect)

    # draw the lines
    pygame.draw.line(screen,color='Black',start_pos=(100 + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        end_pos=(100 + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5),
                        width=2)
    pygame.draw.line(screen,color='Black',start_pos=(200 + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        end_pos=(200 + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5),
                        width=2)
    pygame.draw.line(screen,color='Black',start_pos=(5 + (SCREEN_WIDTH - BOARD_SIZE)/2, 100 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        end_pos=((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, 100 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        width=2)
    pygame.draw.line(screen,color='Black',start_pos=(5 + (SCREEN_WIDTH - BOARD_SIZE)/2, 200 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        end_pos=((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, 200 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                        width=2)

def check_win_or_draw(X,Y,player_token):
    index = [0,1,2]
    index.remove(X)
    if X == Y: #check the right diagonal
        if board[index[0]][index[0]] == player_token_symbol[player_token] and board[index[1]][index[1]] == player_token_symbol[player_token]:
            return 'win', (5 + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2) , ((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5)
    
    if (X+Y) == 2: #check the left diagonal
        if board[index[0]][2-index[0]] == player_token_symbol[player_token] and board[index[1]][2-index[1]] == player_token_symbol[player_token]:
            return 'win' , (5 + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5) , ((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2)

    row = board[X][:]
    column = [board[i][Y] for i in range(len(board[:][Y]))]

    if player_token_symbol[player_token*-1] in row or None in row: #check the column
        if player_token_symbol[player_token*-1] in column or None in column: #check the row
            if any(None in row for row in board):
                return 'next move', None, None
            else:
                return 'draw', None, None
        else:
            # check column
            return 'win', (5 + (SCREEN_WIDTH - BOARD_SIZE)/2, 100*Y + 50 + (SCREEN_HEIGHT - BOARD_SIZE)/2) , ((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, 100*Y + 50 + (SCREEN_HEIGHT - BOARD_SIZE)/2)
    else:
        # check row
        return 'win', (100*X + 50 + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2) , (100*X + 50 + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5)

def reset_game():
    global board, player_token, game_status

    initialize_game()

    board = [[None]*3,[None]*3,[None]*3]
    player_token = 1
    game_status = 'live'


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
                    x = x - (SCREEN_WIDTH - BOARD_SIZE)/2
                    y = y - (SCREEN_HEIGHT - BOARD_SIZE)/2
                    X = math.floor(x/100)
                    Y = math.floor(y/100)
                    
                    if board[X][Y] is None:
                        button_rect = pygame.Rect(X*100 + (SCREEN_WIDTH - BOARD_SIZE)/2, Y*100 + (SCREEN_HEIGHT - BOARD_SIZE)/2, (X+1)*100 + (SCREEN_WIDTH - BOARD_SIZE)/2, (Y+1)*100 + (SCREEN_HEIGHT - BOARD_SIZE)/2)
                        if player_token_symbol[player_token] == 'cross':
                            screen.blit(x_image,button_rect)
                            board[X][Y] = 'cross'
                        elif player_token_symbol[player_token] == 'dot':
                            screen.blit(o_image,button_rect)
                            board[X][Y] = 'dot'
                        
                        outcome, start, end = check_win_or_draw(X=X, Y=Y, player_token=player_token)
                        if outcome == 'win':
                            pygame.draw.line(screen,color='Red',start_pos=start, end_pos=end, width= 4)
                            win_font = pygame.font.Font(None,60)
                            win_surface = win_font.render(f'{player_token_symbol[player_token]} WINS', True,player_token_color[player_token])
                            win_rect = win_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                            game_over_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                            game_over_screen.set_alpha(140)
                            game_over_screen.fill('Grey')
                            screen.blit(game_over_screen, (0,0))
                            screen.blit(win_surface,win_rect)
                            game_status = 'over'
                        elif outcome == 'draw':
                            draw_rect = draw_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
                            draw_font = pygame.font.Font(None,60)
                            draw_surface = draw_font.render('DRAW', True,'Blue')
                            game_over_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                            game_over_screen.set_alpha(140)
                            game_over_screen.fill('Grey')
                            screen.blit(game_over_screen, (0,0))
                            screen.blit(draw_surface,draw_rect)
                            game_status = 'over'

                        player_token = player_token*-1

    pygame.display.update()

    if game_status == 'over':
        time.sleep(2)
        reset_game()


pygame.quit()