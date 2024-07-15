import pygame
import math
import time

SCREEN_WIDTH = 950
SCREEN_HEIGHT = 600
PLAYAREA_WIDTH = 900
PLAYAREA_HEIGHT = 500
BODY_SIZE = 50
MOVEMENT_SPEED = BODY_SIZE/2
MOVEMENT_TIME = 0.25
APPLE_LIFE = 2
APPLE_FADE = 0.25
APPLE_SIZE = 40

game_status = 'over'
start_time = 0
score = 0

class Snake_element(pygame.sprite.Sprite):

    def __init__(self,type,behind=None):
        super().__init__()

        if type == 'head':
            self.move = [MOVEMENT_SPEED,0]
            self.pos = [100,100]
            self.rect = pygame.Rect(self.pos[0],self.pos[1],BODY_SIZE,BODY_SIZE)
            self.image = pygame.Surface((BODY_SIZE,BODY_SIZE))
            self.image.fill('Red')
            self.has_moved_once = False
        else:
            self.move = behind.move

    def player_input(self):

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.move = [0,-MOVEMENT_SPEED]
            if not self.has_moved_once:
                self.move_element(reset=True)
                self.has_moved_once = True
        elif keys[pygame.K_DOWN]:
            self.move = [0,MOVEMENT_SPEED]
            if not self.has_moved_once:
                self.move_element(reset=True)
                self.has_moved_once = True    
        elif keys[pygame.K_RIGHT]:
            self.move = [MOVEMENT_SPEED,0]
            if not self.has_moved_once:
                self.move_element(reset=True)
                self.has_moved_once = True
        elif keys[pygame.K_LEFT]:
            self.move = [-MOVEMENT_SPEED,0]
            if not self.has_moved_once:
                self.move_element(reset=True)
                self.has_moved_once = True

    def color_element(self):
        if self.move == [MOVEMENT_SPEED,0]:
            self.image.fill('Red')
        elif self.move == [-MOVEMENT_SPEED,0]:
            self.image.fill('Blue')
        elif self.move == [0,MOVEMENT_SPEED]:
            self.image.fill('Yellow')
        elif self.move == [0,-MOVEMENT_SPEED]:
            self.image.fill('Green')
    
    def move_element(self,reset=False):
        self.pos = [pos+shift for pos,shift in zip(self.pos,self.move)]
        self.rect.x,self.rect.y = self.pos

        if reset:
            pygame.time.set_timer(movement_timer,int(1000*MOVEMENT_TIME))

    def update(self):
        self.player_input()
        self.color_element()

class Apples(pygame.sprite.Sprite):

    def __init__(self,x_pos,y_pos,fade = False):
        super().__init__()

        self.image = pygame.image.load('Graphics/apple.png').convert_alpha()
        self.image = pygame.transform.scale(self.image,(APPLE_SIZE,APPLE_SIZE))
        self.rect = pygame.Rect(x_pos,y_pos,APPLE_SIZE,APPLE_SIZE)
        self.timer = pygame.time.get_ticks()/1000
        self.alpha = 255
        self.fade = fade
    
    def alpha_update(self):
        if self.fade:
            self.alpha = self.alpha - round(255/(APPLE_LIFE/APPLE_FADE))
            self.image.set_alpha(self.alpha)

    def destroy(self):
        self.kill()
    
    def update(self):
        pass
        




pygame.init()
fps = 60

#define the game window
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
playarea_size = (PLAYAREA_WIDTH,PLAYAREA_HEIGHT)
playarea_rect = pygame.Rect(((SCREEN_WIDTH - PLAYAREA_WIDTH)/2,(SCREEN_HEIGHT - PLAYAREA_HEIGHT)/2),playarea_size)
playarea_surface = pygame.Surface(size=playarea_size)
playarea_surface.fill('Olive')

#change the name that appears on the pygame window
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()

movement_timer = pygame.USEREVENT + 1
pygame.time.set_timer(movement_timer,round(1000*MOVEMENT_TIME))
apple_timer = pygame.USEREVENT + 2
pygame.time.set_timer(apple_timer,round(1000*APPLE_FADE))

def display_intro_screen():
    screen.fill('Grey')
    snake_img = pygame.image.load('Graphics/snake_image.png').convert_alpha()
    snake_img = pygame.transform.rotozoom(snake_img,0,1.25)
    snake_rect = snake_img.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

    heading_font = pygame.font.Font(None,60)
    heading_surface = heading_font.render('SNAKE 2D', True,'Green')
    heading_rect = heading_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT/2 - 200)))

    message_font = pygame.font.Font(None,40)
    message_surface = message_font.render('Press SPACEBAR to play', True,'Black')
    message_rect = message_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT/2 + 200)))

    screen.blit(snake_img,snake_rect)
    screen.blit(heading_surface,heading_rect)
    screen.blit(message_surface,message_rect)

def display_outro_screen():
    screen.fill('Grey')
    snake_img = pygame.image.load('Graphics/snake_image.png').convert_alpha()
    snake_img = pygame.transform.rotozoom(snake_img,0,1.2)
    snake_rect = snake_img.get_rect(center = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

    heading_font = pygame.font.Font(None,60)
    heading_surface = heading_font.render('GAME OVER', True,'Blue')
    heading_rect = heading_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT/2 - 200)))
    
    score_font = pygame.font.Font(None,50)
    score_surface = score_font.render(f'SCORE : {score}', True,'Black')
    score_rect = score_surface.get_rect(midtop = heading_rect.midbottom)
    score_rect.y = score_rect.y + 20

    message_font = pygame.font.Font(None,40)
    message_surface = message_font.render('Press SPACEBAR to play again', True,'Black')
    message_rect = message_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT/2 + 150)))

    screen.blit(snake_img,snake_rect)
    screen.blit(heading_surface,heading_rect)
    screen.blit(score_surface,score_rect)
    screen.blit(message_surface,message_rect)

def reset_game():
    initialize_game()

    score = 0
    # draw the player and start the game

def display_score(x,y,size=25,color='Grey'):
    global score, start_time
    curr_time = round(pygame.time.get_ticks() / 1000)
    score = score + (curr_time - start_time)
    score_font = pygame.font.Font(None,size)
    score_surf = score_font.render(f'Score : {score}', False ,color)
    score_rect = score_surf.get_rect(midleft = (x,y))

    screen.blit(score_surf,score_rect)

snake = pygame.sprite.GroupSingle()
snake.add(Snake_element(type='head'))

apple = pygame.sprite.GroupSingle()
apple.add(Apples(300,300))

run = True
# initialize_game()
while run:
    clock.tick(fps) #set the maximum frame rate

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                if game_status == 'live':
                    game_status = 'over'
                else:
                    start_time = round(pygame.time.get_ticks() / 1000)
                    game_status = 'live'
                    score = 0
                    snake.add(Snake_element(type='head'))
            
        if event.type == pygame.KEYUP and snake.sprite.has_moved_once:
            snake.sprite.has_moved_once = False
        
        if game_status == 'live':
            if event.type == movement_timer:
                snake.sprite.move_element()

            if event.type == apple_timer:
                apple.sprite.alpha_update()
    
    #display on each frame
    if game_status == 'live':
        if (snake.sprite.rect.midbottom[1] > (SCREEN_HEIGHT + PLAYAREA_HEIGHT)/2) or (snake.sprite.rect.midright[0] > (SCREEN_WIDTH + PLAYAREA_WIDTH)/2) or (snake.sprite.rect.midtop[1] < (SCREEN_HEIGHT - PLAYAREA_HEIGHT)/2) or (snake.sprite.rect.midleft[0] < (SCREEN_WIDTH - PLAYAREA_WIDTH)/2):
            game_status = 'over'
        else:
            game_status = 'live'
            screen.fill('Black')
            screen.blit(playarea_surface, playarea_rect)

            # heading on the screen
            heading_font = pygame.font.Font(None,30)
            heading_surface = heading_font.render('SNAKE', True,'Green')
            heading_rect = heading_surface.get_rect(center = (SCREEN_WIDTH/2,(SCREEN_HEIGHT - PLAYAREA_HEIGHT)/4))
            screen.blit(heading_surface,heading_rect)
            display_score(x = (SCREEN_WIDTH - PLAYAREA_WIDTH)/2,y = (SCREEN_HEIGHT - PLAYAREA_HEIGHT)/4)

            snake.update()
            snake.draw(screen)

            apple.draw(screen)
            apple.update()
        
    else:
        if start_time == 0:
            # game start screen
            display_intro_screen()
        else:
            # end game screen
            display_outro_screen()

    pygame.display.update()


pygame.quit()