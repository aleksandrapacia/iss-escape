import pygame



class Button:
    def __init__(self, x: int, y: int, image: pygame.Surface, scale: float):
        width = image.get_width()
        height = image.get_height()

        self.image = pygame.transform.scale(
            image, (int(width * scale), int(height * scale))
        )

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

        self.rect.topleft = (x, y)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
