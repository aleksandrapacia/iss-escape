import pygame
import sys
from station import ISS

# Screen settings
(width, height) = (600, 487)
screen = pygame.display.set_mode((width, height))
screen_rect = screen.get_rect()

# Caption
pygame.display.set_caption('ISS Escape')

# Background 
background = pygame.image.load('bg.jpg')

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

    all_keys = pygame.key.get_pressed()
    if all_keys[pygame.K_LEFT]:
        iss.pos_x -= 0.15
        print('left')
    elif all_keys[pygame.K_RIGHT]:
        iss.pos_x += 0.15
        print('right')


    # Keeping player on screen
    if iss.pos_x < 0:
        iss.pos_x = 0
    if iss.pos_x > 420:
        iss.pos_x = 420

    screen.blit(background, (0,0))
    screen.blit(iss.texture, (iss.pos_x, iss.pos_y)) 
    pygame.display.flip()
