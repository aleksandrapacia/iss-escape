import pygame

class ISS():
    def __init__(self, screen,):
        """ Reading an image and downloading rect """
        self.image = pygame.image.load('iss.png')
        self.rect = self.image.get_rect()
        self.screen = screen
        
    def render(self):
        self.screen.blit(self.image, self.rect)
