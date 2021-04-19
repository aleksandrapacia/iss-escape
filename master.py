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
iss = ISS(screen)

# Main loop
running = True
while running:
    all_event = pygame.event.get()
    for event in all_event:
        if event.type == pygame.QUIT:
            sys.exit()
    pygame.display.flip()

    iss.render() 
