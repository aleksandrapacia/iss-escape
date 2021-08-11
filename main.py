  
import pygame
import sys

from pygame.constants import WINDOWFOCUSGAINED
from station import Station
import pygame.mixer
import random
from enemy import Enemy
from bullet import Bullet
import math

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 486
STATION_HEIGHT = 380
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

# Time sec
start_time = 0
clock = pygame.time.Clock()

# Enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file).convert_alpha()
enemy_texture_mask = pygame.mask.from_surface(enemy_texture)
enemy_rect = enemy_texture.get_rect()
enemies: list[Enemy] = []

# Bullets
bulletX = 90
bulletY = 390
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png").convert_alpha()
# Bullet mask
bullet_texture_mask = pygame.mask.from_surface(bullet_texture)
bullet_rect = bullet_texture.get_rect()
ox = bulletX+station.pos_x
oy = STATION_HEIGHT+10


bullets: list[Bullet] = []

# Caption
pygame.display.set_caption("ISS Escape")

# Background
background_texture = pygame.image.load("assets/textures/bg.png").convert()
y = 0

# Shot sound
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")

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

# # #
black = (0, 0, 0)
white = (255, 255, 255)
menu_title = font2.render('ISS Escape', True, black)
short_information = font.render('Click on the screen to start', True, black)
# # # 

# Main loop
menu = True
while True:
    while menu:
        all_event = pygame.event.get()
        for event in all_event:
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    menu = False
        screen.fill(white)
        screen.blit(menu_title, (200, 5))
        screen.blit(short_information, (10, 100))
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

        # Collision
        for bullet in bullets:
            offset = (int(enemy.pos_x) - int(bullet.pos_x), int(enemy.pos_y) - int(bullet.pos_y))
            result = bullet_texture_mask.overlap(enemy_texture_mask, offset)
            if result:
                score+=1 
                print(f'c={score}')
                bullets.remove(bullet)
                enemies.remove(enemy)

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