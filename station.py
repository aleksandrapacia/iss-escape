import pygame

class ISS(pygame.sprite.Sprite):
    def __init__(self, screen, pos_x: float, pos_y: float, texture: pygame.Surface):
        """ Reading an image and downloading rect """
        self.image = pygame.image.load('iss.png')
        self.screen = screen
        self.rect = self.image.get_rect()
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture

    def render(self):
        self.screen.blit(self.image, self.rect)