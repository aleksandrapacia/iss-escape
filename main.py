from numpy import true_divide
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
intro_background = pygame.image.load('assets/textures/intro.png')
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

menu_button_levels = pygame.image.load('assets/textures/menu_button.png').convert()
menu_button_levels = MenuButton(514, 2, menu_button_levels, 0.5)
# pause button
pause_button = pygame.image.load('assets/textures/pause_button.png').convert()
pause_button = PauseButton(514, 2, pause_button, 0.5)

# |||sounds|||
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# |||fonts|||
largetext = pygame.font.Font('freesansbold.ttf',80)
smalltext = pygame.font.Font('freesansbold.ttf',20)
mediumtext = pygame.font.Font('freesansbold.ttf',40)
# |||'Score:' position|||
text_x = int(227)
text_y = int(177)

# |||colors|||
black = (0, 0, 0)
white = (255, 255, 255)
violet = (155, 96, 214)

# menu
menu_title = largetext.render('ISS Escape', True, (45, 48, 144))

# mouse
mouse = pygame.mouse.get_pos()
score = Bullet.score = 0
def show_score(x, y):
        score_value = mediumtext.render("Score: " + str(Bullet.score), True, black)
        screen.blit(score_value, (x, y))

def p_again_collision():
        screen.fill(white)
        # title of the 'window'
        afterGame_info = mediumtext.render('Game finished', True, black, violet)
        text_position = (178, 58)
        screen.blit(afterGame_info, text_position)
        # shwoing scores
        show_score(text_x, text_y)
        # drawind bottons
        restart_button.draw(screen)
        menu_button.draw(screen)


# main loop
def intro_loop():
    '''starts intro, first called function'''
    intro=True
    start_time = 0
    while intro:
        all_event = pygame.event.get()
        for event in all_event:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                a, b = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if start_button.rect.collidepoint(a, b):
                        intro = False
                        print('start butto clicked')
                        # game_loop()
                    if quit_button.rect.collidepoint(a, b):
                        sys.exit()
                    if levels_button.rect.collidepoint(a, b):
                        intro=False
                        levels()

        screen.blit(intro_background, (0,0))
        start_button.draw(screen)
        quit_button.draw(screen)
        levels_button.draw(screen)
        pygame.display.update()


def levels():
    levels=True
    while levels:
        all_event = pygame.event.get()
        for event in all_event:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                a, b = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if menu_button.rect.collidepoint(a, b):
                        intro_loop().run()

        screen.blit(intro_background, (0,0))
        menu_button_levels.draw(screen)
        levels_title = largetext.render('Levels', True, white)
        text_position = (178, 4)
        screen.blit(levels_title, text_position)
        pygame.display.update()


# running main function (contains main loop)
intro_loop()
#  T O D O S
#TODO: pausing game after station got hit or the bullet flew off the screen     
#TODO: add button restart  
#TODO: change the way buttons look
#TODO: change click sound
#TODO: add levels