import pygame


class Station(pygame.sprite.Sprite):
    def __init__(self, pos_x: float, pos_y: float, texture: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
        self.rect = texture.get_rect()
