import pygame

class ISS():
    def __init__(self, screen, pos_x: int, pos_y: int, texture: pygame.Surface):
        """ Reading an image and downloading rect """
        self.image = pygame.image.load('iss.png')
        self.rect = self.image.get_rect()
        self.screen = screen
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
        
    def render(self):
        self.screen.blit(self.image, self.rect)
