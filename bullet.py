import pygame


class Bullet:
    def __init__(
        self, pos: float, posy: float, texture: pygame.Surface, speed: float
    ):
        self.pos_x = pos
        self.pos_y = posy
        self.texture = texture
        self.speed = speed

    def move(self):
        self.pos_y -= self.speed
