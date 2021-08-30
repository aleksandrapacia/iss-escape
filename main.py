import pygame
import sys

from pygame.constants import MOUSEBUTTONDOWN
from station import Station
import pygame.mixer
import random

from enemy import Enemy
from bullet import Bullet
from button import Button


# initialazing pygame
pygame.init()

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 486
STATION_HEIGHT = 371
BULLET_SPEED = 5
ENEMY_SPEED = 1.02
HW, HH = SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2

# screen
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
intro_background = pygame.image.load('assets/textures/intro.png').convert()
pygame.display.set_caption("ISS Escape")

# station
station_file = open("assets/textures/iss.png")
station_texture = pygame.image.load(station_file)
station = Station(200, int(STATION_HEIGHT), station_texture)
#station's mask
station_texture_mask = pygame.mask.from_surface(station_texture)
station_rect = station_texture.get_rect()

# enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file).convert_alpha()
# enemy's mask
enemy_texture_mask = pygame.mask.from_surface(enemy_texture)
enemy_rect = enemy_texture.get_rect()
enemies: list[Enemy] = []

# bullets
bulletX = 90
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png").convert_alpha()
bullets: list[Bullet] = []
# bullet's mask
bullet_texture_mask = pygame.mask.from_surface(bullet_texture)
bullet_rect = bullet_texture.get_rect()
ox = bulletX+station.pos_x
oy = STATION_HEIGHT+10

# time setup
clock = pygame.time.Clock()

# start button
start_button = pygame.image.load('assets/textures/start_button.png').convert()
start_button = Button(230, 200, start_button, 0.9)
# light start button
start_light = pygame.image.load('assets/textures/start_light.png').convert()
start_light = Button(230, 200, start_light, 0.9)

# quit button
quit_button = pygame.image.load('assets/textures/quit_button.png').convert()
quit_button = Button(230, 300, quit_button, 0.9 )
# light quit button
quit_light = pygame.image.load('assets/textures/quit_light.png').convert()
quit_light = Button(230, 300, quit_light, 0.9)

# levels button
levels_button = pygame.image.load('assets/textures/levels_button.png').convert()
levels_button = Button(230, 400, levels_button, 0.9)
# light levels' button
levels_light = pygame.image.load('assets/textures/levels_light(2).png').convert()
levels_light = Button(230, 400, levels_light, 0.9)

# restart button
restart_button = pygame.image.load('assets/textures/restart_light.png').convert()
restart_button = Button(215, 300, restart_button, 1)
# light restart button
restart_light = pygame.image.load('assets/textures/restart_light.png').convert()
restart_light = Button(215, 300, restart_light, 1 )

# menu button
menu_button = pygame.image.load('assets/textures/menu_button.png').convert()
menu_button = Button(215, 220, menu_button, 1)
# light menu buttons
menu_button_light = pygame.image.load('assets/textures/light_menu.png').convert()
menu_button_light_levels = Button(514, 2, menu_button_light, 0.5)
menu_button_light = Button(215, 220, menu_button_light, 1)
menu_button_levels = pygame.image.load('assets/textures/menu_button.png').convert()
menu_button_levels = Button(514, 2, menu_button_levels, 0.5)

# pause button
pause_button = pygame.image.load('assets/textures/pause_button.png').convert()
pause_button = Button(514, 2, pause_button, 0.5)
# light pause button
pause_light = pygame.image.load('assets/textures/pause_light.png').convert()
pause_light = Button(514, 2, pause_light, 0.5) 

#retry button
retry_button = pygame.image.load('assets/textures/retry_button.png').convert()
retry_button = Button(215, 320, retry_button, 1)

# sounds
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# fonts
largetext = pygame.font.SysFont('Arial',80)
smalltext = pygame.font.SysFont('freesansbold.ttf',50)
mediumtext = pygame.font.SysFont('freesansbold.ttf',30)

# score text's position
text_x = int(227)
text_y = int(177)

# colors
black = (0, 0, 0)
white = (255, 255, 255)
violet = (155, 96, 214)

# menu title
menu_title = largetext.render('ISS Escape', True, (45, 48, 144))

# mouse
mouse = pygame.mouse.get_pos()
score = Bullet.score = 0

# background setup
bg = pygame.image.load('assets/textures/bg.png').convert()
y_axis=0


def show_score(x, y):
        score_value = mediumtext.render("Score: " + str(Bullet.score), True, white)
        screen.blit(score_value, (x, y))

class Status(object):
    def __init__(self):
        self.game = False
        self.pause = False
        self.pause_after_collision = False
        self.levels = False
        self.intro = False

    def pause_button_clicked(self, pause, game, intro):
        self.pause=True
        while self.pause:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking on the buttons
                    if pygame.mouse.get_pressed()[0]:
                        if restart_button.rect.collidepoint(x, y):
                            click_sound.play()
                            game=True
                            pause=False
                            st.game_loop(game=True, pause_after_collision=False, pause=False)
                        if menu_button.rect.collidepoint(x, y):
                            click_sound.play()
                            intro=True
                            game=False
                            st.intro_loop(game=False, intro=True, pause_after_collision=False)
                        
            screen.blit(intro_background, (0,0))
            pause_title = largetext.render('Paused', True, white)
            pause_title_position = (190, 4)
            screen.blit(pause_title, pause_title_position)
            restart_button.draw(screen)
            menu_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button.rect.collidepoint(mouse):
                menu_button_light.draw(screen)
            if restart_button.rect.collidepoint(mouse):
                restart_light.draw(screen)
            pygame.display.update(screen_rect)

    # what happens after collision: between enemy and station, enemy and the edge
    # of the screen
    def pause_after_collision_loop(self):
        pause_after_collision=True
        while pause_after_collision:
            print(Bullet.score)
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking on the buttons
                    if pygame.mouse.get_pressed()[0]:
                        if menu_button.rect.collidepoint(x, y):
                            intro=True
                            pause_after_collision=False
                            click_sound.play()
                            st.intro_loop(game=False, intro=True, pause_after_collision=False)

            screen.blit(intro_background, (0,0))
            pause_title = largetext.render('Loss', True, white)
            pause_title_position = (230, 4)
            screen.blit(pause_title, pause_title_position)
            score_text = mediumtext.render(f'Scores gained in this round: {Bullet.score}', True, white)
            scoretext_position = (160, 100)
            screen.blit(score_text, scoretext_position)
            menu_button.draw(screen)
            retry_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button.rect.collidepoint(mouse):
                menu_button_light.draw(screen)
            pygame.display.update(screen_rect)


    # menu (intro)
    def intro_loop(self, game, intro, pause_after_collision):
        intro=True
        while intro:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking buttons
                    if pygame.mouse.get_pressed()[0]:
                        if start_button.rect.collidepoint(x, y):
                            click_sound.play()
                            game=True
                            intro=False
                            pause_after_collision=False
                            st.game_loop(game=True, pause_after_collision=False, pause=False)
                        if quit_button.rect.collidepoint(x, y):
                            click_sound.play()
                            sys.exit()
                        if levels_button.rect.collidepoint(x, y):
                            click_sound.play()
                            self.levels=True
                            self.intro=False
                            st.levels_loop(levels=True, intro=False)

            screen.blit(intro_background, (0,0))

            intro_title = largetext.render('ISS Escape', True, white)
            text_position = (134, 4)
            screen.blit(intro_title, text_position)
            start_button.draw(screen)
            quit_button.draw(screen)
            levels_button.draw(screen)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if levels_button.rect.collidepoint(mouse):
                levels_light.draw(screen)
            if start_button.rect.collidepoint(mouse):
                start_light.draw(screen)
            if quit_button.rect.collidepoint(mouse):
                quit_light.draw(screen)
            pygame.display.update(screen_rect)

    # information about levels and list of them 
    def levels_loop(self, levels, intro):
        levels=True
        while self.levels:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    # clicking buttons
                    if pygame.mouse.get_pressed()[0]:
                        # going to intro loop
                        if menu_button_levels.rect.collidepoint(x, y):
                            click_sound.play()
                            intro=True
                            leves=False
                            st.intro_loop(game=False, intro=True, pause_after_collision=False)
                            
                    
            screen.blit(intro_background, (0,0))
            menu_button_levels.draw(screen)
            levels_title = largetext.render('Levels', True, white)
            text_position = (178, 4)
            screen.blit(levels_title, text_position)

            mouse = pygame.mouse.get_pos()
            # changing buttons' colors after cursor touches them
            if menu_button_levels.rect.collidepoint(mouse):
                menu_button_light_levels.draw(screen)
            pygame.display.update(screen_rect)

    # main loop of the game
    def game_loop(self,game,pause_after_collision,pause):
        y_axis=0
        start_time = 0
        while game:
            # scrolling screen
            rel_y = y_axis % bg.get_rect().height
            screen.blit(bg, (0 , rel_y - bg.get_rect().height))
            y_axis-=1
            show_score(5, 5)
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    bullet = Bullet(
                    bulletX + int(station.pos_x),
                    STATION_HEIGHT + 10,
                    bullet_texture,
                    BULLET_SPEED, 0.0)
                    bullets.append(bullet)
                    shot_sound.play()

                x,y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    # clicking pause button
                    if pause_button.rect.collidepoint(x, y):
                        click_sound.play()
                        pause=True
                        st.pause_button_clicked(pause=True, game=False, intro=False)
        
            # creating multiple enemies'
            for i in range(10):
                enemy = Enemy(random.randrange(67, 520), -20, enemy_texture, ENEMY_SPEED)
                start_time+=1
                if start_time > 200:
                   enemies.append(enemy)
                   start_time = 0

            # enemies' and bullets' movements
            for bullet in bullets:
                bullet.move() 
            for enemy in enemies:
                enemy.move()

            # when game is finished (after collision)
            for enemy in enemies:
                if enemy.pos_y > SCREEN_HEIGHT:
                    game=False
                    pause_after_collision=True
                    st.pause_after_collision_loop()

                if enemy.pos_y == station.pos_y:
                   game=False
                   pause_after_collision
                   st.pause_after_collision_loop()

                # collision between bullet and enemy
                for bullet in bullets:
                    offset = (int(enemy.pos_x) - int(bullet.pos_x), int(enemy.pos_y) - int(bullet.pos_y))
                    result = bullet_texture_mask.overlap(enemy_texture_mask, offset)
                    if result:
                        Bullet.score+=1 
                        print(f'c={score}')
                        bullets.remove(bullet)
                        enemies.remove(enemy)

                # collision between station and enemies
                for enemy in enemies:
                    offset = (int(enemy.pos_x) - int(station.pos_x), int(enemy.pos_y) - int(station.pos_y))
                    result = station_texture_mask.overlap(enemy_texture_mask, offset)
                    if result:
                        game=False
                        pause_after_collision=True
                        st.pause_after_collision_loop()

            # station's movement
            all_keys = pygame.key.get_pressed()
            if all_keys[pygame.K_LEFT]:
                station.pos_x -= 4
            elif all_keys[pygame.K_RIGHT]:
                station.pos_x += 4

            # removing enemy when it goes off screen
            for bullet in bullets[:]:
                if bullet.pos_x < 0:
                    bullets.remove(bullet)
            for i in range(len(bullets)):
                bullet = bullets[i]

            # keeping player on screen
            if station.pos_x < 0:
                station.pos_x = 0
            if station.pos_x > 420:
                station.pos_x = 420

            # displaying bullets
            for bullet in bullets:
                screen.blit(bullet_texture, pygame.Rect(bullet.pos_x, bullet.pos_y, 0, 0))
    
            # displaying enemies
            for enemy in enemies:
                screen.blit(enemy.texture, pygame.Rect(enemy.pos_x, enemy.pos_y, 0, 0))
    
            # displaying station
            screen.blit(station.texture, (station.pos_x, station.pos_y))

            # drawing pause button on screen
            mouse = pygame.mouse.get_pos()
            pause_button.draw(screen)
            if pause_button.rect.collidepoint(mouse):
                pause_light.draw(screen)

            pygame.display.update(screen_rect)

            # timing game
            clock.tick(60)
    
    def x(self, intro, pause_after_collision):
        if intro==True:
            pause_after_collision=False

st = Status()
while True:
    st.intro_loop(game=True, intro=True, pause_after_collision=False)
    st.x()
    pygame.display.update()