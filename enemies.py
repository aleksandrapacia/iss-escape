import pygame
import pygame.sprite


class Enemy:
    def __init__(
        self, pos_x: float, pos_y: float, texture: pygame.Surface, speed: float
    ):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
        self.speed = speed

        self.counter = 0

    def move(self):
        distance = 7000
        if self.counter >= 0 and self.counter <= distance:
            self.pos_y += self.speed
        elif self.counter >= distance and self.counter <= distance * 2:
            self.pos_y -= self.speed
        else:
            self.counter = 0

        self.counter += 1
