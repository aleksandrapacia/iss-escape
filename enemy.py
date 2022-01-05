from numpy import exp
import pygame

Explosion = [pygame.image.load('assets//textures//exp1.png'), pygame.image.load('assets//textures//exp2.png'), 
            pygame.image.load('assets//textures//exp3.png'), pygame.image.load('assets//textures//exp4.png'),
            pygame.image.load('assets//textures//exp5.png')]

class Enemy(pygame.sprite.Sprite):
    def __init__(
        self,
        pos_x: int,
        pos_y: int,
        texture: pygame.Surface,
        speed: int,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.texture = texture
        self.speed = speed
        self.rect = texture.get_rect(
            center = (pos_x, pos_y)
        )
        self.animation_count = 0
        self.animation_frames = 10
        self.animation = False

    def move(self):
        self.pos_y += self.speed

    def start_animation(self):
        self.animation = True

    def update(self):

        if self.animation:
            image_index = self.animation_count // self.animation_frames
            self.animation_count += 1

            if image_index < len(Explosion):
                self.surf = Explosion[image_index]
                self.rect = self.surf.get_rect(center = self.rect.center)

            else:
                self.kill()

        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()
