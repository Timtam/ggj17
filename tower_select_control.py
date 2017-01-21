import pygame

from commons import *
from control import Control

class TowerSelectControl(Control):
	def __init__(self, centerx, centery):
		super(TowerSelectControl, self).__init__(pygame.Rect(centerx - 32, centery - 32, 64, 64))
		self.enabled = False
		self.background = get_common().get_image('assets/ui/tower_select.png')
		self.towers = []
		self.towers.append(get_common().get_image('assets/level/towers/watertower.png'))
		self.towers.append(get_common().get_image('assets/level/towers/soundtower.png'))
		self.towers.append(get_common().get_image('assets/level/towers/lighttower.png'))

	def _draw(self, screen):
		if not self.enabled: return
		screen.blit(self.background, self.rect)
		screen.blit(self.towers[0], (self.rect.centerx - self.towers[0].get_width() / 2, self.rect.top + 25 - self.towers[0].get_height()))
		screen.blit(self.towers[1], (self.rect.left + 5 - self.towers[1].get_width() / 2, self.rect.bottom - 5 - self.towers[1].get_height()))
		screen.blit(self.towers[2], (self.rect.right - 5 - self.towers[2].get_width() / 2, self.rect.bottom - 5 - self.towers[2].get_height()))
