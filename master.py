import pygame
import sys
from station import ISS
from pygame.sprite import Group
from pygame.locals import *
import pygame.mixer

pygame.init()
clock = pygame.time.Clock()

# Screen settings
(width, height) = (600, 487)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Bullets
bullets = []
bullet_picture = pygame.image.load('bullet.png').convert_alpha()

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
            bullets.append([event.pos[1]-190, 400])

    # ISS moves
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        iss.pos_x -= 0.15
        print('left')
    elif all_keys[pygame.K_RIGHT]:
        iss.pos_x += 0.15
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
    screen.blit(iss.texture, (iss.pos_x, iss.pos_y)) 
    screen.blit(iss.texture, (my, 500))
    pygame.display.flip()
