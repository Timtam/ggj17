import pygame
from random import randint
from commons import *



class Field:
	def __init__(self, screen, ftype, x, y):
		self.x = x
		self.y = y
		self.screen = screen
		self.type  = ftype
		#0 - grass
		if self.type == 0:
			self.sprite = get_common().get_image('assets/level/tiles/grass.png')
		#1 - way
		elif self.type == 1:
			self.sprite = get_common().get_image('assets/level/tiles/dirt.png')
		else:
			stone = randint(1, 10)
			self.sprite = get_common().get_image('assets/level/decoration/rock_' + str(stone) + '.png')
			
		self.tower = None
		self.enemies=[]

	def newEnemy(self, enemy):
		self.enemies.append(enemy())

	def setTower(self, tower):
		self.tower = tower

	def getType(self):
		return self.type

	def render(self):
		if self.tower == None:
			#TODO!!
			surf = pygame.Surface((32, 32))
			surf.blit(self.sprite, (0,0))
			return surf

		tower_surf = self.tower.render()
		surf = pygame.Surface(tower_surf.get_size(), pygame.SRCALPHA)
		surf.blit(self.sprite, (tower_surf.get_width() / 2 - 16, tower_surf.get_height() - 32))
		surf.blit(tower_surf, (0, 0))
		return surf

	def update(self, level):
		if self.tower!=None:
			self.tower.update(level, self.x, self.y)
		for enemy in self.enemies:
			enemy.update(level, self.x, self.y)
