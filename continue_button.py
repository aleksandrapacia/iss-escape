import pygame

class ContinueButton(pygame.surface.Surface):
	def __init__(self, x, y, image, scale):
		width = image.get_width()
		height = image.get_height()

		self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

		self.rect = self.image.get_rect()

		self.rect.topleft = (x, y)

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))