import pygame
import math
import time

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
BOARD_SIZE = 600 #square board
CELL_SIZE = BOARD_SIZE/8

#initializing a 8*8 grid
board = [[None]*8 for i in range(8)]
game_over = False

#keeps track of the colour of the player whose turn it is
player_token = 1 #white plays first
player_token_color = {1 : 'black', -1 : 'white'}

#start the working of pygame
pygame.init()
fps = 60

#define the game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption('Othello') #change the name that appears on the pygame window

# define the black button
black_button_image = pygame.image.load('Graphics/black_button.png').convert_alpha()
black_button_image = pygame.transform.scale(black_button_image, (BOARD_SIZE*0.125, BOARD_SIZE*0.125))

# define the white button 
white_button_image = pygame.image.load('Graphics/white_button.png').convert_alpha()
white_button_image = pygame.transform.scale(white_button_image, (BOARD_SIZE*0.125, BOARD_SIZE*0.125))

# player move display
player_move_font = pygame.font.Font(None,30)
player_move_surface = player_move_font.render('BLACK to move', True,'Black') #first to move
player_move_rect = player_move_surface.get_rect(center = (SCREEN_WIDTH/2,(3*SCREEN_HEIGHT + BOARD_SIZE)/4))

# score display
SCORE_black_X = 100
SCORE_black_Y = 70
SCORE_white_X = 700
SCORE_white_Y = 70

def count_score():
    global board, black_score, white_score

    black_score = 0
    white_score = 0
    for i in range(8):
        for j in range(8):
            if board[i][j] == 1:
                black_score = black_score + 1
            elif board[i][j] == -1:
                white_score = white_score + 1
            else:
                pass
    
    return black_score, white_score

def draw_token(X,Y,token_color):
    button_rect = pygame.Rect(X*CELL_SIZE + (SCREEN_WIDTH - BOARD_SIZE)/2,
                                                Y*CELL_SIZE + (SCREEN_HEIGHT - BOARD_SIZE)/2,
                                                (X+1)*CELL_SIZE + (SCREEN_WIDTH - BOARD_SIZE)/2,
                                                (Y+1)*CELL_SIZE + (SCREEN_HEIGHT - BOARD_SIZE)/2)
    if token_color == 1:
        screen.blit(black_button_image,button_rect)
    elif token_color == -1:
        screen.blit(white_button_image,button_rect)
    else:
        pass

def draw_board():
    global board

    for i in range(8):
        for j in range(8):
            draw_token(i,j,board[i][j])

def initialize_game():
    global board
    """create the screen, the board and draw the lines"""
    # do not declare or initialize any image or button in thi space
    screen.fill('Grey')

    # define the game heading
    heading_font = pygame.font.Font(None,60)
    heading_surface = heading_font.render('OTHELLO', True,'Olive')
    heading_rect = heading_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT - BOARD_SIZE)/4))

    # game board
    board_image = pygame.image.load('Graphics/board.jpg').convert()
    board_image = pygame.transform.scale(board_image, (BOARD_SIZE, BOARD_SIZE))

    # paste the board onto the screen
    screen.blit(board_image,((SCREEN_WIDTH - BOARD_SIZE)/2,(SCREEN_HEIGHT - BOARD_SIZE)/2))
    screen.blit(heading_surface,heading_rect)

    # draw the lines
    for i in range(1,8,1):
        pygame.draw.line(screen,color='Black',start_pos=(CELL_SIZE*i + (SCREEN_WIDTH - BOARD_SIZE)/2, 5 + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                            end_pos=(CELL_SIZE*i + (SCREEN_WIDTH - BOARD_SIZE)/2, (SCREEN_HEIGHT + BOARD_SIZE)/2 - 5),
                            width=2)
        pygame.draw.line(screen,color='Black',start_pos=(5 + (SCREEN_WIDTH - BOARD_SIZE)/2, CELL_SIZE*i + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                            end_pos=((SCREEN_WIDTH + BOARD_SIZE)/2 - 5, CELL_SIZE*i + (SCREEN_HEIGHT - BOARD_SIZE)/2),
                            width=2)
    
    # draw the 4 tokens
    board[3][3] = -1
    board[4][4] = -1
    board[3][4] = 1
    board[4][3] = 1

    draw_board()

def flip(flipped_token):
    global board
    for token in flipped_token:
        board[token[0]][token[1]] = board[token[0]][token[1]]*-1

def inbounds(variable):
    if variable >= 0 and variable <=7:
        return True
    else:
        return False

def token_series_valid(X,Y,X_inc,Y_inc,match_token,end_token):
    global board
    this_token = [[X,Y]]
    X_new = X + X_inc
    Y_new = Y + Y_inc
    if not inbounds(X_new) or not inbounds(Y_new) or board[X_new][Y_new] == None:
        return []
    elif board[X_new][Y_new] == match_token:
        token_series = token_series_valid(X_new,Y_new,X_inc,Y_inc,match_token,end_token)
        if token_series == []:
            return []
        else:
            token_series.append(this_token[0])
            return token_series
    elif board[X_new][Y_new] == end_token:
        return this_token

def check_for_flips(X,Y,player_token,status):
    global board
    opponent_token = player_token*-1
    valid_neighbours =[]
    top = inbounds(X-1)
    bottom = inbounds(X+1)
    left = inbounds(Y-1)
    right = inbounds(Y+1)

    # check around the token
    if top:
        if left:
            if board[X-1][Y-1] == opponent_token:
                valid_neighbours = valid_neighbours + token_series_valid(X-1,Y-1,X_inc=-1,Y_inc=-1,match_token=opponent_token,end_token=player_token)
        if board[X-1][Y] == opponent_token:
            valid_neighbours = valid_neighbours + token_series_valid(X-1,Y,X_inc=-1,Y_inc=0,match_token=opponent_token,end_token=player_token)
        if right:
            if board[X-1][Y+1] == opponent_token:
                valid_neighbours = valid_neighbours + token_series_valid(X-1,Y+1,X_inc=-1,Y_inc=1,match_token=opponent_token,end_token=player_token)
    
    if bottom:
        if right:
            if board[X+1][Y+1] == opponent_token:
                valid_neighbours = valid_neighbours + token_series_valid(X+1,Y+1,X_inc=1,Y_inc=1,match_token=opponent_token,end_token=player_token)
        if board[X+1][Y] == opponent_token:
            valid_neighbours = valid_neighbours + token_series_valid(X+1,Y,X_inc=1,Y_inc=0,match_token=opponent_token,end_token=player_token)
        if left:
            if board[X+1][Y-1] == opponent_token:
                valid_neighbours = valid_neighbours + token_series_valid(X+1,Y-1,X_inc=1,Y_inc=-1,match_token=opponent_token,end_token=player_token)

    if right:
        if board[X][Y+1] == opponent_token:
            valid_neighbours = valid_neighbours + token_series_valid(X,Y+1,X_inc=0,Y_inc=1,match_token=opponent_token,end_token=player_token)
    if left:
        if board[X][Y-1] == opponent_token:
            valid_neighbours = valid_neighbours + token_series_valid(X,Y-1,X_inc=0,Y_inc=-1,match_token=opponent_token,end_token=player_token)

    valid_neighbours = [tokens for tokens in valid_neighbours if tokens != []]

    if valid_neighbours == []:
        return False
    else:
        if status == 'play':
            flip(valid_neighbours)
        elif status == 'check':
            pass
        # for token in valid_neighbours:
        #     print(token)
        #     _ = check_for_flips(token[0],token[1],player_token=player_token)
        return True

def valid_move_present(player_token):
    global board

    move_available = False
    i = 0
    while (i < 8) and not move_available:
        j = 0
        while (j < 8) and not move_available:
            if board[i][j] is None:
                if check_for_flips(i,j,player_token,status='check'):
                    move_available = True
            
            j = j+1
        i = i+1

    return move_available

def display_player_move(player_token):
    if player_token == 1:
        player_move_surface = player_move_font.render('BLACK to move', True,'Black')
    else:
        player_move_surface = player_move_font.render('WHITE to move', True,'White')
    screen.blit(player_move_surface,player_move_rect)

def check_game_over():
    global board, game_over

    black_score,white_score = count_score()

    if not game_over:
        if black_score == 0 or white_score == 0 or (black_score + white_score) == 64:
            game_over = True
        else:
            game_over = False

def display_score():
    black_score, white_score = count_score()

    score_font = pygame.font.Font(None,25)

    black_score_surface = score_font.render(f'BLACK : {black_score}', True, 'Black')
    white_score_surface = score_font.render(f'WHITE : {white_score}', True, 'White')

    black_score_rect = black_score_surface.get_rect(topleft = (SCORE_black_X, SCORE_black_Y))
    white_score_rect = white_score_surface.get_rect(topright = (SCORE_white_X, SCORE_white_Y))

    #clear screen
    black_score_surface.fill('Grey')
    white_score_surface.fill('Grey')

    screen.blit(black_score_surface,black_score_rect)
    screen.blit(white_score_surface,white_score_rect)

    black_score_surface = score_font.render(f'BLACK : {black_score}', True, 'Black')
    white_score_surface = score_font.render(f'WHITE : {white_score}', True, 'White')

    screen.blit(black_score_surface,black_score_rect)
    screen.blit(white_score_surface,white_score_rect)

def display_game_end():
    result_font = pygame.font.Font(None,60)
    black_score,white_score = count_score()
    if black_score > white_score:
        result_surface = result_font.render('BLACK WINS', True, 'Black')
    elif black_score < white_score:
        result_surface = result_font.render('WHITE WINS', True, 'White')
    else:
        result_surface = result_font.render('TIE', True, 'Grey')

    result_rect = result_surface.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    game_over_screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    game_over_screen.set_alpha(140)
    game_over_screen.fill('Grey')
    screen.blit(game_over_screen, (0,0))
    screen.blit(result_surface,result_rect)

    # time.sleep(2)

    message_font = pygame.font.Font(None,40)
    message_surface = message_font.render('Click to Restart game', True, 'Black')
    message_rect = message_surface.get_rect(center = (SCREEN_WIDTH/2,50 + SCREEN_HEIGHT/2))
    screen.blit(message_surface,message_rect)

def reset_game():
    global board, game_over

    board = [[None]*8 for i in range(8)]
    game_over = False
    initialize_game()

run = True
initialize_game()

while run:
    clock.tick(fps) #set the maximum frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x,y = pygame.mouse.get_pos()

            if game_over:
                reset_game()
            else:
                if x < (SCREEN_WIDTH - BOARD_SIZE)/2 or x > (SCREEN_WIDTH + BOARD_SIZE)/2 or y < (SCREEN_HEIGHT - BOARD_SIZE)/2 or y > (SCREEN_HEIGHT + BOARD_SIZE)/2:
                    pass
                    # out of the board
                else:
                    x = x - (SCREEN_WIDTH - BOARD_SIZE)/2
                    y = y - (SCREEN_HEIGHT - BOARD_SIZE)/2
                    X = math.floor(x/CELL_SIZE)
                    Y = math.floor(y/CELL_SIZE)
                    
                    if board[X][Y] is None:
                        if check_for_flips(X,Y,player_token,status='play'):
                            board[X][Y] = player_token
                            draw_board()

                            if valid_move_present(player_token*-1):
                                # opponent plays
                                player_token = player_token*-1
                                # clear the message screen
                                player_move_surface.fill('Grey')
                                screen.blit(player_move_surface,player_move_rect)
                            elif valid_move_present(player_token):
                                # same player plays again
                                pass
                            else:
                                game_over =True
                            
                            check_game_over()

                        else:
                            # invalid move
                            pass

            if game_over:
                display_game_end()   
            


    if not game_over:
        display_player_move(player_token= player_token)
        display_score()

    
    pygame.display.update()




pygame.quit()