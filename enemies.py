import pygame
import pygame.sprite

class Enemy01(pygame.sprite.Sprite):
    def __init__(self, screen, enemyX: float, enemyY: float, texture: pygame.Surface):
        pygame.sprite.Sprite.__init__(self)
        self.enemyImg = pygame.image.load('stone_2.png')
        self.rect = self.enemyImg.get_rect()
        self.enemyX = enemyY
        self.enemyY = enemyY
        self.texture = texture
        self.counter = 0

    def move(self):
        self.rect = self.enemyImg.get_rect()
        '''enemies movement'''
        distance = 7000
        speed = 0.2
        if self.counter >= 0 and self.counter <= distance:
            self.enemyY += speed
        elif self.counter >= distance and self.counter <= distance*2:
            self.enemyY -= speed
        else:
            self.counter = 0

        self.counter += 1
