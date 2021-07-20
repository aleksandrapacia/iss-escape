import pygame

class Enemy01(pygame.sprite.Sprite):
    def __init__(self, screen, enemyX: float, enemyY: float, texture: pygame.Surface):
        self.enemyImg = pygame.image.load('stone_2.png')
        self.rect = self.enemyImg.get_rect()
        self.enemyX = enemyX
        self.enemyY = enemyY
        self.texture = texture
