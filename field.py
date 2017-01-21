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

	def newEnemy(self, enemy):
		self.enemies.append(enemy())

	def setTower(self, tower):
		self.tower = tower

	def getType(self):
		return self.type

	def render_underground(self):
		return self.sprite
	def render_tower(self):
		return self.tower.render()


	def update(self, level):
		if self.tower!=None:
			self.tower.update(level, self.x, self.y)
		for enemy in self.enemies:
			enemy.update(level, self.x, self.y)
