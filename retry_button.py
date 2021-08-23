import pygame

class RetryButton(pygame.surface.Surface):
	def __init__(self, x, y, image, scale):
		self.width = image.get_width()
		self.height = image.get_height()

		self.image = pygame.transform.scale(image, (int(self.width * scale), int(self.height * scale)))

		self.rect = self.image.get_rect()

		self.rect.topleft = (x, y)

	def draw(self, surface):
		surface.blit(self.image, (self.rect.x, self.rect.y))