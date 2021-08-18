  
import pygame
import sys

from pygame.constants import MOUSEBUTTONDOWN
from station import Station
import pygame.mixer
import random

from pause_button import PauseButton
from enemy import Enemy
from bullet import Bullet
from button import Button
from quit_button import QuitButton
from levels_button import LevelsButton
from restart_button import RestartButton
from menu_button import MenuButton


# initialazing pygame
pygame.init()

# constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 486
STATION_HEIGHT = 371
BULLET_SPEED = 5
ENEMY_SPEED = 1.02
HW, HH = SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2

# events' main function
def events():
    # pause button
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Bullets' class
            bullet = Bullet(
                bulletX + int(station.pos_x),
                STATION_HEIGHT + 10,
                bullet_texture,
                BULLET_SPEED, 0.0
            )
            bullets.append(bullet)
            shot_sound.play()
# screen
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()
# caption
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
bulletY = 390
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png").convert_alpha()
bullets: list[Bullet] = []
# bullet's mask
bullet_texture_mask = pygame.mask.from_surface(bullet_texture)
bullet_rect = bullet_texture.get_rect()
ox = bulletX+station.pos_x
oy = STATION_HEIGHT+10

# time
clock = pygame.time.Clock()

#   ////|||||||||||\\\\
#  ///s t o r a g e \\\\
#  \\\\|||||||||||||////

# background
background_texture = pygame.image.load("assets/textures/bg.png").convert()
y = 0

# |||buttons|||
# start button
start_button = pygame.image.load('assets/textures/start_button.png').convert()
start_button = Button(240, 200, start_button, 0.6)
# quit button
quit_button = pygame.image.load('assets/textures/quit_button.png').convert()
quit_button = QuitButton(240, 300, quit_button, 0.6 )
# levels' button
levels_button = pygame.image.load('assets/textures/levels_button.png').convert()
levels_button = LevelsButton(240, 400, levels_button, 0.6)
# restart's button
restart_button = pygame.image.load('assets/textures/restart_button.png').convert()
restart_button = RestartButton(215, 300, restart_button, 1)
# menu's button
menu_button = pygame.image.load('assets/textures/menu_button.png').convert()
menu_button = MenuButton(215, 220, menu_button, 1)
# pause button
pause_button = pygame.image.load('assets/textures/pause_button.png').convert()
pause_button = PauseButton(300, 40, pause_button, 1)

# |||sounds|||
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# |||fonts|||
small_boring = pygame.font.Font('freesansbold.ttf', 32) #font
big_boring = pygame.font.Font('freesansbold.ttf', 50) #font2

# |||'Score:' position|||
text_x = int(227)
text_y = int(177)

# |||colors|||
black = (0, 0, 0)
white = (255, 255, 255)
violet = (155, 96, 214)

# |||menu|||
menu_title = big_boring.render('ISS Escape', True, (45, 48, 144))
short_information = small_boring.render('Click on the screen to start', True, (45, 48, 144))

# mouse
mouse = pygame.mouse.get_pos()
score = Bullet.score = 0
def show_score(x, y):
        score_value = small_boring.render("Score: " + str(Bullet.score), True, black)
        screen.blit(score_value, (x, y))

# pausing 
pause = False

def p_again_collision():
        screen.fill(white)
        # title of the 'window'
        afterGame_info = small_boring.render('Game finished', True, black, violet)
        text_position = (178, 58)
        screen.blit(afterGame_info, text_position)
        # shwoing scores
        show_score(text_x, text_y)
        # drawind bottons
        restart_button.draw(screen)
        menu_button.draw(screen)


# main loop
def game():
    # showing scores after lose
    show_score(text_x, text_y)
    # scores counter
    # defining menu as True boolean to make menu run (if menu=False then game is True)
    game=True
    # timing game
    start_time = 0
    while True: # TODO: spróbuj dwa sposoby : funkcja menu() lub usunięcie tego < while True i tylko while menu
        while game:
            all_event = pygame.event.get()
            for event in all_event:
                if event.type == pygame.QUIT:
                    sys.exit()
                # buttons' events
                if event.type == MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        # starting game
                        if start_button.rect.collidepoint(x, y):
                            if event.button == 1:
                                click_sound.play()
                                game=False
                        # quitting game
                        if quit_button.rect.collidepoint(x, y):
                            if event.button == 1:
                               sys.exit()
                        # checking levels
                        if levels_button.rect.collidepoint(x, y):
                            if event.button == 1:
                                click_sound.play()
                                print('level1, level2, level3')
                        if restart_button.rect.collidepoint(x, y):
                            if event.button == 1:
                                click_sound.play()
                        if menu_button.rect.collidepoint(x, y):
                            if event.button == 1:
                                click_sound.play()
                                menu=True
                        
            # menu's color                   
            screen.fill(violet)
            # displaying main title: 'ISS Escape'
            screen.blit(menu_title, (160, 5))
            # drawing buttons
            start_button.draw(screen)
            quit_button.draw(screen)
            levels_button.draw(screen)

            # timing game
            clock.tick(30)
            #updating
            pygame.display.update()

        events()

        # scrolling background
        rel_y = y % background_texture.get_rect().height
        screen.blit(background_texture, (0, rel_y - background_texture.get_rect().height))
        if rel_y < 475:
            screen.blit(background_texture, (0, rel_y))
        y-=2

        # creating multiple enemies'
        for i in range(4):
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

        # when game is finished
        for enemy in enemies:
            if enemy.pos_y > SCREEN_HEIGHT:
                p_again_collision()

               # |RESTART MENU|
               # pausing game
            if enemy.pos_y == station.pos_y:
                p_again_collision()

                # |RESTART MENU|
                # pausing game

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
                    p_again_collision()

        # station's movement
        all_keys = pygame.key.get_pressed()
        if all_keys[pygame.K_LEFT]:
            station.pos_x -= 4
        elif all_keys[pygame.K_RIGHT]:
            station.pos_x += 4

        # removing enemy if it goes off screen
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
        pause_button.draw(screen)
        pygame.display.flip()
        # timing game
        clock.tick(60)


# running main function (contains main loop)
running=True
while running:
    game()

#  T O D O S
#TODO: pausing game after station got hit or the bullet flew off the screen     
#TODO: add button restart  
#TODO: change the way buttons look
#TODO: change click sound
#TODO: add levels