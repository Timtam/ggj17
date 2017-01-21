import pygame

from commons import *
from control import Control

class TowerSelectControl(Control):
	def __init__(self, centerx, centery):
		super(TowerSelectControl, self).__init__(pygame.Rect(centerx - 64, centery - 64, 128, 128))
		self.enabled = False
		self.background = pygame.transform.scale(pygame.image.load('assets/ui/tower_select.png'), (128, 128))

	def _draw(self, screen):
		if not self.enabled: return
		screen.blit(self.background, self.rect)
