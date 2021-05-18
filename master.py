import pygame
import sys
from station import ISS
from pygame.sprite import Group
from pygame.locals import *
import pygame.mixer
import random
from enemies import Enemies
import random

pygame.init()
clock = pygame.time.Clock()

# Screen settings
(width, height) = (600, 487)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Bullets
bullets = []
bullet_picture = pygame.image.load('bullet.png').convert_alpha()
bulletX = 92
bulletY = 390

# Enemies
enemy_img = pygame.image.load('stone_2.png')
enemyX = random.randint(0, 600)
enemyY = random.randint(0, 200)
enemy_change = 0

def enemy(x, y):
    screen.blit(enemy_img, (x,y))
# Caption
pygame.display.set_caption('ISS Escape')

# Background 
background = pygame.image.load('bg.jpg')

# Shot sound 
shot = pygame.mixer.Sound('shot.wav')

# Station
iss_file = open('iss.png')
texture_station = pygame.image.load(iss_file)
iss = ISS(screen, 200, 380, texture_station)

# Main loop
running = True
while running:
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            shot.play()
            bullets.append([bulletX+iss.pos_x, bulletY])

    # ISS moves
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        iss.pos_x -= 0.5
        print('left')
    elif all_keys[pygame.K_RIGHT]:
        iss.pos_x += 0.5
        print('right')


    clock.tick(200)

    my, mx = pygame.mouse.get_pos()
    
    for b in range(len(bullets)):
        bullets[b][1] -= 10
    # Iterate over a slice copy if you want to mutate a list.
    for bullet in bullets[:]:
        if bullet[0] < 0:
            bullets.remove(bullet)

    # Keeping player on screen
    if iss.pos_x < 0:
        iss.pos_x = 0
    if iss.pos_x > 420:
        iss.pos_x = 420

    screen.blit(background, (0,0))
    for bullet in bullets:
        screen.blit(bullet_picture, pygame.Rect(bullet[0], bullet[1], 0, 0))
    
    
    enemy(enemyX, enemyY)
    screen.blit(iss.texture, (iss.pos_x, iss.pos_y)) 
    screen.blit(iss.texture, (mx, 500))
    pygame.display.flip()