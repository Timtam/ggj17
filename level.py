from field import Field
from enemies.ghost import Ghost
import tower
from towers import water_tower
import pygame
from controls import *
from commons import *
import timeit
import time

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
		self.cash_icon = get_common().get_image('assets/ui/crystal.png')
		#self.enemy_icon = get_common().get_image('assets/ui/enemy.png')
		#self.time_icon = get_common().get_image('assets/ui/time.png')
		#self.health_icon = get_common().get_image('assets/ui/health.png')

		self.cash=300
		self.enemy_types = (Ghost, Ghost, Ghost)
		self.total_enemies = len(self.enemy_types)
		self.killed_enemies = 0
		self.wave_started = time.clock()
		self.current_lives = 30

		for i in range(self.gridsize):
			self.grid.append([])
			for j in range(self.gridsize):
				self.grid[i].append(Field(self.screen, 0, i, j))

		for field in self.level:
			self.grid[field[0]][field[1]] = Field(self.screen, 1, field[0], field[1])

		self.grid[0][12].enemies.append(Ghost(timeit.default_timer()))

		panel_width = self.gridsize * self.spriteSize
		panel = PanelControl((self.screen.get_width() - panel_width) / 2, 0, panel_width, self.field_y)
		self.controls.append(panel)
		self.cash_text_control = TextControl(50, 23, '0')
		panel.add_child_control(self.cash_text_control)
		self.enemies_text_control = TextControl(190, 23, '0/0')
		panel.add_child_control(self.enemies_text_control)
		self.timer_text_control = TextControl(340, 23, '00:00')
		panel.add_child_control(self.timer_text_control)
		self.health_text_control = TextControl(470, 23, '0')
		panel.add_child_control(self.health_text_control)
		self.tower_select = TowerSelectControl(0, 0, self)
		self.controls.append(self.tower_select)


	def leave(self):
		pass

	def render(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				tmpsprite = self.grid[i][j].render()
				self.screen.blit(tmpsprite, (i * self.spriteSize + self.field_x - (tmpsprite.get_width() - self.spriteSize) / 2, (j * self.spriteSize) - (tmpsprite.get_height() - self.spriteSize) + self.field_y))
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				for enemy in self.grid[i][j].enemies:
					surf, coord = enemy.render()
					self.screen.blit(surf, (coord[0] + i * self.spriteSize + self.field_x, coord[1] + (j * self.spriteSize) + self.field_y))
		for control in self.controls:
			control.draw(self.screen)
		self.screen.blit(self.cash_icon, (self.field_x + 17, 17))
		#self.screen.blit(self.enemy_icon, (self.field_x + 157, 17))
		#self.screen.blit(self.time_icon, (self.field_x + 307, 17))
		#self.screen.blit(self.health_icon, (self.field_x + 437, 17))

	def handle_ev(self, event):
		if event.type == pygame.MOUSEBUTTONUP and not self.tower_select.enabled:
			pos = pygame.mouse.get_pos()
			i = (pos[0] - self.field_x) / self.spriteSize
			j = (pos[1] - self.field_y) / self.spriteSize
			if not ( i < 0 or i > (self.gridsize - 1) or j < 0 or j > (self.gridsize - 1) ):
				field = self.grid[i][j]
				if field.getType() == 0 and field.tower == None:
					self.tower_select.rect.centerx = i * self.spriteSize + self.field_x + self.spriteSize / 2
					self.tower_select.rect.centery = j * self.spriteSize + self.field_y + self.spriteSize / 2
					self.tower_select.enable()
					self.new_tower_coord = (i, j)
		if self.tower_select.enabled and self.tower_select.selected_tower != None:
			self.tower_select.enabled = False
			i, j = self.new_tower_coord
			tower = self.tower_select.selected_tower
			tower.init()
			self.grid[i][j].setTower(tower)


	def update(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				self.grid[i][j].update(self)
		self.cash_text_control.set_text(str(self.cash))
		self.enemies_text_control.set_text(str(self.killed_enemies) + " / " + str(self.total_enemies))
		wave_time = int(time.clock() - self.wave_started)
		s = wave_time % 60
		m = (wave_time - s) / 60
		s = str(s).zfill(2)
		m = str(m).zfill(2)
		self.timer_text_control.set_text(m + ':' + s)
		self.health_text_control.set_text(str(self.current_lives))
		for control in self.controls:
			control.update()
