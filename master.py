import pygame
import sys
from station import ISS
from pygame.sprite import Group
from pygame.locals import *
import pygame.mixer
import random
import random
import math
from enemies import Enemy01

pygame.init()
clock = pygame.time.Clock()

# Screen settings
(width, height) = (600, 487)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Station
iss_file = open('iss.png')
texture_station = pygame.image.load(iss_file)
iss = ISS(screen, 200, 380, texture_station)

# Enemy01 -- specification 
enemy01_file = open('stone_2.png')
texture_enemy01 = pygame.image.load(enemy01_file)
enemy01 = Enemy01(screen, random.randrange(0, 600), 0, texture_enemy01)

# Bullets
bullets = []
bullet_picture = pygame.image.load('bullet.png').convert_alpha()
bulletX = 90
bulletY = 390

# Caption
pygame.display.set_caption('ISS Escape')

# Background 
background = pygame.image.load('bg.jpg')

# Shot sound 
shot = pygame.mixer.Sound('shot.wav')

# Enemies container
all_enemies = pygame.sprite.Group()

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
    elif all_keys[pygame.K_RIGHT]:
        iss.pos_x += 0.5

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
    screen.blit(enemy01.texture, (enemy01.enemyX, enemy01.enemyY))
    screen.blit(iss.texture, (iss.pos_x, iss.pos_y)) 
    pygame.display.flip()