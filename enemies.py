import pygame
import os
from pygame.sprite import Group

pygame.init()

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.counter = 0

    def move(self):
        distance = 500
        speed = 1

        if self.counter >= 0 and self.counter <= distance:
            self.rect.y += speed

        self.counter += 1