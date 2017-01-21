import pygame

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
		else:
			self.sprite = get_common().get_image('assets/level/tiles/dirt.png')

		self.tower = None
		self.enemies=[]

	def setTower(self, tower):
		self.tower = tower

	def getType(self):
		return self.type

	def render(self):
		if self.tower == None:
			return self.sprite

		tower_surf = self.tower.render()
		surf = pygame.Surface(tower_surf.get_size(), pygame.SRCALPHA)
		surf.blit(self.sprite, (tower_surf.get_width() / 2 - 16, tower_surf.get_height() - 32))
		surf.blit(tower_surf, (0, 0))
		return surf

	def update(self, level):
		if self.tower!=None:
			self.tower.update(level, self.x, self.y)
