import pygame
pygame.init()

stone = pygame.image.load('stone.png')
 
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = stone
        self.image.get_rect()
     
enemy_list = pygame.sprite.Group()
enemy_list.add(enemy)