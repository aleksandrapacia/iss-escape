import pygame


class Bullet:
    def __init__(
        self, pos_x: float, pos_y: float, texture: pygame.Surface, speed: float
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
        self.speed = speed

    def move(self):
        self.pos_y -= self.speed
