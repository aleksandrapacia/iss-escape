import pygame


class Station:
    def __init__(self, pos_x: float, pos_y: float, texture: pygame.Surface):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
