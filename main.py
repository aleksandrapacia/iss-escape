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
SCREEN_HEIGHT = 487
STATION_HEIGHT = 380
BULLET_SPEED = 1
ENEMY_SPEED = 1.02

def events():
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Bullets' class
            bullet = Bullet(
                bulletX + station.pos_x,
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
station = Station(200, STATION_HEIGHT, station_texture)

# Time sec
start_time = 0
clock = pygame.time.Clock()

# Enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file)
enemies: list[Enemy] = []

# Bullets
bulletX = 90
bulletY = 390
bullet_file = open("assets/textures/bullet.png")
bullet_texture = pygame.image.load("assets/textures/bullet.png")
bullets: list[Bullet] = []

# Caption
pygame.display.set_caption("ISS Escape")

# Background
background_texture = pygame.image.load("assets/textures/bg.png").convert()
y = 0

# Shot sound
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")
explosion_sound = pygame.mixer.Sound("assets/sounds/explosion.wav")

score = 0

# Main loop
running = True
while running:
    events()
    rel_y = y % background_texture.get_rect().height 
    screen.blit(background_texture, (0, rel_y - background_texture.get_rect().height))
    y+=1
            # Checking whether the bullet hits the enemy
             # hits = pygame.Rect.collidelist(enemies, bullets) < -- (?)
             # if hits:
                 #print('c')          

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

    pygame.display.flip()
    clock.tick(60)
    