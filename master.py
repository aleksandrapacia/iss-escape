import pygame
import sys
from station import ISS

# Screen settings
(width, height) = (730, 487)
screen = pygame.display.set_mode((width, height))

# Caption
pygame.display.set_caption('ISS Escape')

# Background 
background = pygame.image.load('bg.jpg')
screen.blit(background, (0,0))

# Station
iss_file = 'iss.png'
texture_station = pygame.image.load(iss_file)
iss = ISS(screen, 50, 50, texture_station)

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
    elif all_keys[pygame.K_RIGHT]:
        iss.pos_x += 0.15
    elif all_keys[pygame.K_UP]:
        iss.pos_y -= 0.15
    elif all_keys[pygame.K_DOWN]:
        iss.pos_y += 0.15

    screen.blit(iss.texture, (iss.pos_x, iss.pos_y))
    pygame.display.flip()
