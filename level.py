from field import Field
from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.barrel import Barrel
from enemies.golem import Golem
import tower
from towers import water_tower
import pygame
from controls import *
from commons import *
import time

class Level:
	def __init__(self, screen):
		self.decoration = [
		(1, 14), (14, 3), (14, 4)]
		self.level = [
			(2, 12), (3, 12), (3, 11), (3, 10), (4, 10), (5, 10), (6, 10), (6, 9), (6, 8), (6, 7), (5, 7),
			(4, 7), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (8, 4),
			(8, 5), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 13),
			(11, 13), (12, 13), (13, 13), (13, 12), (13, 11), (13, 10), (13, 9), (13, 8), (12, 8), (12, 7),
			(12, 6), (13, 6), (13, 5)]
		self.level.reverse()
		self.grid        = []
		self.gridsize    = 16
		self.spriteSize  = 32
		self.screen      = screen
		self.field_x     = (self.screen.get_width() - self.spriteSize * self.gridsize) / 2
		self.field_y     = 64
		self.controls    = []
		self.cash_icon = get_common().get_image('assets/ui/crystal.png')
		self.enemy_icon = get_common().get_image('assets/ui/sword.png')
		self.time_icon = get_common().get_image('assets/ui/time.png')
		self.health_icon = get_common().get_image('assets/ui/heart.png')
		#TODO: add new sprite
		self.wave_icon = get_common().get_image('assets/ui/heart.png')

		self.cash=300
		self.bgm = None
		self.waves = [##################BALANCE###############
			('level1.ogg', (
				(12, Skeleton, 3),
			)),
			('level2.ogg', (
				(3, Skeleton, 2, 2), # spawn 5 ghosts with 1s between each, then wait 5 seconds
				(3, Ghost, 4, 2),
				(3, Skeleton, 2, 1),
				(3, Skeleton, 2))),
			('level3.ogg', (
				(12, Skeleton, 2, 2),
				(1, Barrel, 2),
				(2, Ghost, 2, 2),
				(2, Barrel, 1))),
			('level4.ogg', (
				(18, Skeleton, 2, 0.5),
				(5, Barrel, 2),
				(7, Ghost, 1, 3),
				(3, Barrel, 1))),
			('level5.ogg', (
				(10, Skeleton,1,1),
				(10, Ghost,1,2),
				(11, Barrel,1,0.5),
				(1, Golem,1,0.2),
				(13, Ghost,1))), 
			('level6.ogg', (
				(10, Skeleton,0.2,0.4),
				(3, Ghost,1,1),
				(3, Barrel,1,1),
				(3, Skeleton,1,1),
				(3, Barrel,1,1),
				(3, Skeleton,2,1),
				(3, Skeleton,0.4,0.4),
				(3, Barrel,1,0.4),
				(1, Golem,1),
				(3, Skeleton,0.4,0.4),
				(3, Barrel,1,0.4),
				(3, Skeleton,0.4,0.4),
				(3, Barrel,1,0.4),
				(3, Ghost,1,0.4),
				(3, Skeleton,0.4,0.4),
				(5, Barrel,1,0.4),
				(1, Golem,1))), #addGolem
			('level7.ogg', (
				(20, Barrel,1,2),
				(20, Skeleton,1,1),
				(11, Barrel,1,1),
				(20, Ghost,1,2),
				(10, Skeleton,1,2),
				(5, Skeleton,2,2),
				(15, Barrel,1,2),
				(20, Ghost,1,0.2),
				(4, Golem,1))), #addGolem
			('level8.ogg', (
				(20, Skeleton,1,0),
				(20, Barrel,1,2),
				(20, Skeleton,1,1),
				(11, Barrel,1,1),
				(20, Ghost,1,2),
				(10, Skeleton,1,2),
				(5, Skeleton,2,2),
				(15, Barrel,1,2),
				(20, Ghost,1,5),
				(8, Golem,1)))] #addGolem
		self.current_lives = 20
		self.in_wave = False

		for i in range(self.gridsize):
			self.grid.append([])
			for j in range(self.gridsize):
				self.grid[i].append(Field(self.screen, 0, i, j, None, 0))
		latest = self.level[0]
		for i in range(len(self.level)):
			
			
			
			if i == len(self.level) - 1:
				next = self.level[i]
			else:
				next = self.level[i+1]
				
			me   = self.level[i]
				
			if latest[0] == self.level[i][0] and self.level[i][0] == self.level[i+1][0]:
				self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 0, 0)
			elif latest[1] == self.level[i][1] and self.level[i][1] == next[1]:
				self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 0, 90)
			else:
				#dont worry it works - dont touch - dont know how, but its good :)
				#von oben nach links?
				if (me[1] > next[1] and me[0] == next[0] and me[0] > latest[0] and me[1] == latest[1]) or (me[1] > latest[1] and me[0] == latest[0] and me[0] > next[0] and me[1] == next[1]):
					self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 1, 180)
				#von links nach unten?
				elif (me[0] == next[0] and me[0] > latest[0] and me[1] == latest[1] and me[1] < next[1]) or (me[0] == latest[0] and me[0] > next[0] and me[1] == next[1] and me[1] < latest[1]):
					self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 1, 270)
				#von rechts nach unten
				elif (me[1] == next[1] and me[1] < latest[1] and me[0] == latest[0] and me[0] < next[0]) or (me[1] == latest[1] and me[1] < next[1] and me[0] == next[0] and me[0] < latest[0]):
					self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 1, 0)
				#von oben nach rechts
				elif (me[1] > latest[1] and me[0] == latest[0] and me[1] == next[1] and me[0] < next[0]) or (me[1] > next[1] and me[0] == next[0] and me[1] == latest[1] and me[0] < latest[0]):
					self.grid[self.level[i][0]][self.level[i][1]] = Field(self.screen, 1, self.level[i][0], self.level[i][1], 1, 90)
				
			latest = self.level[i]
				
		for field in self.decoration:
			self.grid[field[0]][field[1]] = Field(self.screen, 2, field[0], field[1], 0, 0)

		panel_width = self.gridsize * self.spriteSize
		panel = PanelControl((self.screen.get_width() - panel_width) / 2, 0, panel_width, self.field_y)
		self.controls.append(panel)
		#TODO
		self.cash_text_control = TextControl(50, 23, '0')
		panel.add_child_control(self.cash_text_control)
		self.enemies_text_control = TextControl(150, 23, '0 / 0')
		panel.add_child_control(self.enemies_text_control)
		self.timer_text_control = TextControl(255, 23, '00:00')
		panel.add_child_control(self.timer_text_control)
		self.health_text_control = TextControl(375, 23, '0')
		panel.add_child_control(self.health_text_control)
		self.wave_text_control = TextControl(445, 23, '0')
		panel.add_child_control(self.wave_text_control)
		self.tower_select = TowerSelectControl(0, 0, self)
		self.controls.append(self.tower_select)

		self.paused = False
		self.was_paused = False
		self.pause_start_time = None
		self.pause_panel = PanelControl((self.screen.get_width() - 400) / 2, (self.screen.get_height() - 400) / 2, 400, 400)
		self.pause_panel.add_child_control(TextControl(0, 0, 'Paused'), center = True)
		self.pause_panel.add_child_control(ButtonControl(105, 350, 'Back to main menu', self.back_to_main_clicked))
		self.pause_dim = pygame.transform.scale(get_common().get_image('assets/ui/dim.png'), self.screen.get_size())

		self.current_wave = -1
		self.start_wave_button = ButtonControl(self.field_x + panel_width + 50, self.field_y + 150, 'Start wave', self.start_wave_clicked)

	def leave(self):
		if self.bgm != None:
			self.bgm.Stop()

	def next_wave(self):
		self.start_wave(self.current_wave + 1)

	def start_wave(self, index = 0):
		if self.bgm != None:
			self.bgm.Stop()
		wave = self.waves[index]
		self.current_wave = index
		self.bgm = play_sound_bgm('assets/sound/bgm/' + wave[0])
		play_sound_fx('assets/sound/common/level_start.ogg')
		self.enemy_types = wave[1]
		self.total_enemies = 0
		self.removed_enemies = 0
		self.all_enemies = []
		for e in self.enemy_types:
			self.total_enemies += e[0]
			for i in range(e[0] - 1):
				self.all_enemies.append((e[1], e[2]))
			if len(e) == 4:
				self.all_enemies.append((e[1], e[3]))
			else:
				self.all_enemies.append((e[1], 0))
		self.killed_enemies = 0
		self.wave_started = time.time()
		self.enemy_spawn_index = 0
		self.next_enemy_spawn = time.time()
		self.in_wave = True

	def start_wave_clicked(self):
		self.next_wave()
	def back_to_main_clicked(self):
		get_common().get_main().change_view('MainMenu')

	def remove_enemy(self, enemy):
		self.removed_enemies += 1
		if self.removed_enemies == self.total_enemies:
			play_sound_fx('assets/sound/common/level_win.ogg')
			self.in_wave = False

	def render(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				self.screen.blit(self.grid[i][j].render_underground(), (i * self.spriteSize + self.field_x, j * self.spriteSize + self.field_y))
				if self.grid[i][j].type == 2:
					self.screen.blit(self.grid[i][j].render_deco(), (i * self.spriteSize + self.field_x, j * self.spriteSize + self.field_y))

		for j in range(self.gridsize):
			for i in range(self.gridsize):
				for enemy in self.grid[i][j].enemies:
					surf, coord = enemy.render()
					self.screen.blit(surf, (coord[0] + i * self.spriteSize + self.field_x, coord[1] + (j * self.spriteSize) + self.field_y))
				if self.grid[i][j].tower != None:
					tmpsprite = self.grid[i][j].render_tower()
					self.screen.blit(tmpsprite, (i * self.spriteSize + self.field_x - (tmpsprite.get_width() - self.spriteSize) / 2, (j * self.spriteSize) - (tmpsprite.get_height() - self.spriteSize) + self.field_y))
		for control in self.controls:
			control.draw(self.screen)

		if not self.in_wave:
			self.start_wave_button.draw(self.screen)
		self.screen.blit(self.cash_icon, (self.field_x + 17, 17))
		self.screen.blit(self.enemy_icon, (self.field_x + 117, 17))
		self.screen.blit(self.time_icon, (self.field_x + 217, 17))
		self.screen.blit(self.health_icon, (self.field_x + 337, 17))
		#TODO: calculate
		self.screen.blit(self.wave_icon, (self.field_x + 410, 17))
		if self.paused:
			self.screen.blit(self.pause_dim, (0, 0))
			self.pause_panel.draw(self.screen)

	def handle_ev(self, event):
		if event.type == pygame.MOUSEBUTTONUP and not self.tower_select.enabled and not self.paused:
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
		if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
			if self.paused:
				self.was_paused = True
				self.paused = False
			else:
				self.paused = True
				self.pause_start_time = time.time()
		if self.tower_select.enabled and self.tower_select.selected_tower != None:
			self.tower_select.enabled = False
			i, j = self.new_tower_coord
			tower = self.tower_select.selected_tower
			tower.init()
			self.grid[i][j].setTower(tower, self.level)

	def update(self):
		if not self.paused:
			if self.was_paused:
				self.was_paused = False
				time_delta = time.time() - self.pause_start_time
				for i in range(self.gridsize):
					for j in range(self.gridsize):
						field = self.grid[i][j]
						if field.tower != None:
							field.tower.LastFire += time_delta
						for enemy in field.enemies:
							enemy.start += time_delta
			for i in range(self.gridsize):
				for j in range(self.gridsize):
					self.grid[i][j].update(self)
			if self.in_wave:
				if time.time() >= self.next_enemy_spawn and len(self.all_enemies) > self.enemy_spawn_index:
					firstCoord = self.level[-1]
					enemy = self.all_enemies[self.enemy_spawn_index]
					self.enemy_spawn_index += 1
					new_enemy = enemy[0]()
					new_enemy.init()
					self.grid[firstCoord[0]][firstCoord[1]].enemies.append(new_enemy)
					self.next_enemy_spawn += enemy[1]
				self.enemies_text_control.set_text(str(self.killed_enemies) + " / " + str(self.total_enemies))
				wave_time = int(time.time() - self.wave_started)
				s = wave_time % 60
				m = (wave_time - s) / 60
				s = str(s).zfill(2)
				m = str(m).zfill(2)
				self.timer_text_control.set_text(m + ':' + s)
			self.cash_text_control.set_text(str(self.cash))
			self.wave_text_control.set_text(str(self.current_wave + 1) + ' / ' + str(len(self.waves)))
			self.health_text_control.set_text(str(self.current_lives))
		for control in self.controls:
			control.update()
		if not self.in_wave:
			self.start_wave_button.update()
		if self.paused:
			self.pause_panel.update()
