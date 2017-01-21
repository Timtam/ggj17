from field import Field
import tower
from towers import water_tower
import pygame
from controls import *

class Level:
	def __init__(self, screen):
		self.level = [
			(0, 12), (1, 12), (2, 12), (3, 12), (3, 11), (3, 10), (4, 10), (5, 10), (6, 10), (6, 9), (6, 8), (6, 7), (5, 7), (4, 7),
			(4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (2, 3), (2, 2), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (7, 2),
			(7, 3), (8, 3), (8, 4), (8, 5), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 13),
			(11, 13), (12, 13), (13, 13), (13, 12), (13, 11), (14, 11), (14, 10), (14, 9), (14, 8), (13, 8), (12, 8), (12, 7), (12, 6), (13, 6),
			(13, 5), (13, 4), (13, 3), (12, 3), (12, 2), (12, 1), (13, 1), (14, 1), (15, 1)]
		self.level.reverse()
		self.grid        = []
		self.gridsize    = 16
		self.spriteSize  = 32
		self.screen      = screen
		self.field_x     = (self.screen.get_width() - self.spriteSize * self.gridsize) / 2
		self.field_y     = 64
		self.controls    = []

		for i in range(self.gridsize):
			self.grid.append([])
			for j in range(self.gridsize):
				self.grid[i].append(Field(self.screen, 0, i, j))

		for field in self.level:
			self.grid[field[0]][field[1]] = Field(self.screen, 1, field[0], field[1])

		panel_width = self.gridsize * self.spriteSize
		panel = PanelControl((self.screen.get_width() - panel_width) / 2, 0, panel_width, self.field_y)
		self.controls.append(panel)
		self.tower_select = TowerSelectControl(0,0)
		self.controls.append(self.tower_select)


	def leave(self):
		pass

	def render(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				tmpsprite = self.grid[i][j].render()
				self.screen.blit(tmpsprite, (i * self.spriteSize + self.field_x - (tmpsprite.get_width() - self.spriteSize) / 2, (j * self.spriteSize) - (tmpsprite.get_height() - self.spriteSize) + self.field_y))
		for control in self.controls:
			control.draw(self.screen)

	def handle_ev(self, event):
		if event.type == pygame.MOUSEBUTTONUP and not self.tower_select.enabled:
			pos = pygame.mouse.get_pos()
			i = (pos[0] - self.field_x) / self.spriteSize
			j = (pos[1] - self.field_y) / self.spriteSize
			if not ( i < 0 or i > (self.gridsize - 1) or j < 0 or j > (self.gridsize - 1) ):
				field = self.grid[i][j]
				if field.getType() == 0:
					self.tower_select.rect.centerx = i * self.spriteSize + self.field_x + self.spriteSize / 2
					self.tower_select.rect.centery = j * self.spriteSize + self.field_y + self.spriteSize / 2
					self.tower_select.enable()
					self.new_tower_coord = (i, j)
		if self.tower_select.enabled and self.tower_select.selected_tower != None:
			self.tower_select.enabled = False
			i, j = self.new_tower_coord
			self.grid[i][j].setTower(self.tower_select.selected_tower)


	def update(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				self.grid[i][j].update(self)
		for control in self.controls:
			control.update()
