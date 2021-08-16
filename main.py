import pygame
import sys

from pygame.constants import MOUSEBUTTONDOWN, WINDOWFOCUSGAINED
from station import Station
import pygame.mixer
import random
from enemy import Enemy
from bullet import Bullet
import math

from button import Button
from quit_button import QuitButton
from levels_button import LevelsButton

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 486
STATION_HEIGHT = 371
BULLET_SPEED = 5
ENEMY_SPEED = 1.02

HW, HH = SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2

# Main function
def events():
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
                BULLET_SPEED,
            )
            bullets.append(bullet)
            shot_sound.play()

# Screen settings
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Station
station_file = open("assets/textures/iss.png")
station_texture = pygame.image.load(station_file)
station = Station(200, int(STATION_HEIGHT), station_texture)
station_texture_mask = pygame.mask.from_surface(station_texture)
station_rect = station_texture.get_rect()

# Time sec
start_time = 0
clock = pygame.time.Clock()

# Enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file).convert_alpha()
enemy_texture_mask = pygame.mask.from_surface(enemy_texture)
enemy_rect = enemy_texture.get_rect()
enemies: list[Enemy] = []

# bullets
bulletX = 90
bulletY = 390
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png").convert_alpha()
bullets: list[Bullet] = []

# bullet mask
bullet_texture_mask = pygame.mask.from_surface(bullet_texture)
bullet_rect = bullet_texture.get_rect()
ox = bulletX+station.pos_x
oy = STATION_HEIGHT+10

# Caption
pygame.display.set_caption("ISS Escape")

# Background
background_texture = pygame.image.load("assets/textures/bg.png").convert()
y = 0

# start button
start_button = pygame.image.load('assets/textures/start_button.png').convert()
start_button = Button(240, 200, start_button, 0.6)

# quit button
quit_button = pygame.image.load('assets/textures/quit_button.png').convert()
quit_button = QuitButton(240, 300, quit_button, 0.6 )

# levels button
levels_button = pygame.image.load('assets/textures/levels_button.png').convert()
levels_button = LevelsButton(240, 400, levels_button, 0.6)
# Shot sound
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")
click_sound = pygame.mixer.Sound("assets/sounds/click.wav")

# Fonts' storage
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 50)

# Scores counting
score = 0
text_x = 10
text_y = 10

def show_score(x, y):
    score_value = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_value, (x, y))

#TODO: check this function - why text isn't blited
def play_again():
    text = font.render('Play again?', 50, (10, 8, 14))
    textx = SCREEN_WIDTH / 2 - text.get_width() / 2
    texty = SCREEN_HEIGHT / 2 - text.get_height() / 2
    textx_size = text.get_width()
    texty_size = text.get_height()
    pygame.draw.rect(screen, (255, 255, 255), ((textx - 5, texty - 5),
                                               (textx_size + 10, texty_size +
                                                10)))


# # #
black = (0, 0, 0)
white = (255, 255, 255)
menu_title = font2.render('ISS Escape', True, (45, 48, 144))
short_information = font.render('Click on the screen to start', True, (45, 48, 144))
mouse = pygame.mouse.get_pos()
violet = (155, 96, 214)
# # # 

#TODO: pausing game after station got hit or the bullet flew off the screen        
menu=True
# Main loop
while True:
    while menu:
        all_event = pygame.event.get()
        for event in all_event:
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if pygame.mouse.get_pressed()[0]:
                    if start_button.rect.collidepoint(x, y):
                        if event.button == 1:
                            print('c')
                            click_sound.play()
                            menu=False
                    if quit_button.rect.collidepoint(x, y):
                        if event.button == 1:
                            sys.exit()
                                  
        screen.fill(violet)
        screen.blit(menu_title, (160, 5))
        start_button.draw(screen)
        quit_button.draw(screen)
        levels_button.draw(screen)
        clock.tick(30)
        pygame.display.update()
    events()
    # Scrolling background
    rel_y = y % background_texture.get_rect().height
    screen.blit(background_texture, (0, rel_y - background_texture.get_rect().height))
    if rel_y < 475:
        screen.blit(background_texture, (0, rel_y))
    y-=2

    # Multiply enemies
    for i in range(4):
        enemy = Enemy(random.randrange(67, 520), -20, enemy_texture, ENEMY_SPEED)
        start_time+=1
        if start_time > 200:
            enemies.append(enemy)
            start_time = 0
    # Bullets' and enemies' movements
    for bullet in bullets:
        bullet.move() 
    for enemy in enemies:
        enemy.move()

    # Moments when game is finished
    for enemy in enemies:
        if enemy.pos_y > SCREEN_HEIGHT:
            play_again()
        if enemy.pos_y == station.pos_y:
            play_again()
            

        # Collision
        for bullet in bullets:
            offset = (int(enemy.pos_x) - int(bullet.pos_x), int(enemy.pos_y) - int(bullet.pos_y))
            result = bullet_texture_mask.overlap(enemy_texture_mask, offset)
            if result:
                score+=1 
                print(f'c={score}')
                bullets.remove(bullet)
                enemies.remove(enemy)

        # Collision 2.0
        for enemy in enemies:
            offset = (int(enemy.pos_x) - int(station.pos_x), int(enemy.pos_y) - int(station.pos_y))
            result = enemy_texture_mask.overlap(station_texture_mask, offset)
            if result:
                play_again()

    # Station moves
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        station.pos_x -= 4
    elif all_keys[pygame.K_RIGHT]:
        station.pos_x += 4

    # Removing enemy if it goes off screen
    for bullet in bullets[:]:
        if bullet.pos_x < 0:
            bullets.remove(bullet)
    for i in range(len(bullets)):
        bullet = bullets[i]

    # Keeping player on screen
    if station.pos_x < 0:
        station.pos_x = 0
    if station.pos_x > 420:
        station.pos_x = 420

    # Displayin bullets
    for bullet in bullets:
        screen.blit(bullet_texture, pygame.Rect(bullet.pos_x, bullet.pos_y, 0, 0))
    
    # Displaying enemies' rectangles 
    for enemy in enemies:
        screen.blit(enemy.texture, pygame.Rect(enemy.pos_x, enemy.pos_y, 0, 0))
    
    # Displaying stations' texture
    screen.blit(station.texture, (station.pos_x, station.pos_y))

    # Score displaying 
    show_score(text_x, text_y)

    pygame.display.flip()
    clock.tick(60)