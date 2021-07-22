import pygame
import sys
from station import Station
from pygame.locals import MOUSEBUTTONDOWN
import pygame.mixer
import random
from enemies import Enemy

pygame.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 487

# Screen settings
(width, height) = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Station
station_file = open("assets/textures/iss.png")
station_texture = pygame.image.load(station_file)
station = Station(200, 380, station_texture)

# Enemy
enemy_file = open("assets/textures/stone_2.png")
enemy_texture = pygame.image.load(enemy_file)
enemy = Enemy(random.randrange(0, 600), 0, enemy_texture, 0.2)
enemies: list[Enemy] = []
enemies.append(enemy)  # type hint

# Bullets
bullets: list[list[float]] = []
bullet_texture = pygame.image.load("assets/textures/bullet.png").convert_alpha()
bulletX = 90
bulletY = 390

# Caption
pygame.display.set_caption("ISS Escape")

# Background
background_texture = pygame.image.load("assets/textures/bg.jpg")

# Shot sound
shot_sound = pygame.mixer.Sound("assets/sounds/shot.wav")

# Main loop
running = True
while running:
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            shot_sound.play()
            bullets.append([bulletX + station.pos_x, bulletY])

    # Enemies moves
    for enemy in enemies:
        enemy.move()

    # Station moves
    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        station.pos_x -= 0.5
    elif all_keys[pygame.K_RIGHT]:
        station.pos_x += 0.5

    my, mx = pygame.mouse.get_pos()

    for b in range(len(bullets)):
        bullets[b][1] -= 10
    # Iterate over a slice copy if you want to mutate a list.
    for bullet in bullets[:]:
        if bullet[0] < 0:
            bullets.remove(bullet)

    # Keeping player on screen
    if station.pos_x < 0:
        station.pos_x = 0
    if station.pos_x > 420:
        station.pos_x = 420

    screen.blit(background_texture, (0, 0))
    for bullet in bullets:
        screen.blit(bullet_texture, pygame.Rect(bullet[0], bullet[1], 0, 0))

    screen.blit(enemy.texture, (enemy.pos_x, enemy.pos_y))
    screen.blit(station.texture, (station.pos_x, station.pos_y))
    pygame.display.flip()
