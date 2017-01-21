import pygame

from commons import *
from control import Control
from towers.water_tower import WaterTower
from towers.bass_tower import BassTower
from towers.light_tower import LightTower

class TowerSelectControl(Control):
	def __init__(self, centerx, centery):
		super(TowerSelectControl, self).__init__(pygame.Rect(centerx - 32, centery - 32, 64, 64))
		self.enabled = False
		self.selected_tower = None
		self.background = get_common().get_image('assets/ui/tower_select.png')
		self.towers = []
		self.towers.append(get_common().get_image('assets/level/towers/watertower.png'))
		self.towers.append(get_common().get_image('assets/level/towers/soundtower.png'))
		self.towers.append(get_common().get_image('assets/level/towers/lighttower.png'))
		self.lmb_down = False

	def enable(self):
		self.enabled = True
		self.selected_tower = None
		self.tower_rects = []
		rect = pygame.Rect(0, 0, self.towers[0].get_width(), self.towers[0].get_height())
		rect.centerx = self.rect.centerx
		rect.bottom = self.rect.top + 25
		self.tower_rects.append(rect)
		rect = pygame.Rect(0, 0, self.towers[1].get_width(), self.towers[1].get_height())
		rect.centerx = self.rect.left + 5
		rect.bottom = self.rect.bottom - 5
		self.tower_rects.append(rect)
		rect = pygame.Rect(0, 0, self.towers[2].get_width(), self.towers[2].get_height())
		rect.centerx = self.rect.right - 5
		rect.bottom = self.rect.bottom - 5
		self.tower_rects.append(rect)

	def _draw(self, screen):
		if not self.enabled: return
		screen.blit(self.background, self.rect)
		for i in range(0,3):
			screen.blit(self.towers[i], self.tower_rects[i])

	def _update(self):
		if not self.enabled: return
		lmb, mmb, rmb = pygame.mouse.get_pressed()
		mx, my = pygame.mouse.get_pos()
		if lmb:
			if self.tower_rects[0].collidepoint(mx, my):
				self.selected_tower = WaterTower()
			elif self.tower_rects[1].collidepoint(mx, my):
				self.selected_tower = BassTower()
			elif self.tower_rects[2].collidepoint(mx, my):
				self.selected_tower = LightTower()
			elif not self.rect.collidepoint(mx, my):
				self.lmb_down = True
		if not lmb and self.lmb_down:
			self.enabled = False
			self.lmb_down = False
