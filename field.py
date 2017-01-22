import pygame
from random import randint
from commons import *

UNDERGROUNDTYPE_GRASS      = 0
UNDERGROUNDTYPE_WAY        = 1
UNDERGROUNDTYPE_DECORATION = 2
WAYTYPE_STRAIGHT           = 0
WAYTYPE_CURVE              = 1

class Field:
	def __init__(self, screen, ftype, x, y, waytype, degree):
		self.x = x
		self.y = y
		self.screen = screen
		self.type  = ftype
		self.waytype = waytype
		self.degree = degree
		#0 - grass
		if self.type == 0:
			self.sprite = get_common().get_image('assets/level/tiles/Maptiles_0.png')
		#1 - way
		elif self.type == 1:
			#0 - straight way
			if self.waytype == 0:
				self.sprite = get_common().get_image('assets/level/tiles/Maptiles_2.png')
			elif self.waytype == 1:
				self.sprite = get_common().get_image('assets/level/tiles/Maptiles_1.png')

			self.sprite = self.rot_center(self.sprite, self.degree)
		#2 - decoration
		else:
			if randint(1,2) == 1:
				decoitem = 'wood'
				deconum = randint(1, 3)
			else:
				decoitem = 'rock'
				deconum = randint(1, 10)
			self.sprite = get_common().get_image('assets/level/decoration/' + decoitem + '_' + str(deconum) + '.png')

		self.tower = None
		self.enemies=[]

	def rot_center(self, image, angle):
		orig_rect = image.get_rect()
		rot_image = pygame.transform.rotate(image, angle)
		rot_rect = orig_rect.copy()
		rot_rect.center = rot_image.get_rect().center
		rot_image = rot_image.subsurface(rot_rect).copy()
		return rot_image

	def newEnemy(self, enemy):
		self.enemies.append(enemy())

	def setTower(self, tower, everyWay):
		self.tower = tower
		for i in range(16):
			if (self.x + i, self.y) in everyWay:
				nearestWay = 'right'
				break;
			if (self.x - i, self.y) in everyWay:
				nearestWay = 'left'
				break;
			if (self.x, self.y + i) in everyWay:
				nearestWay = 'down'
				break;
			if (self.x, self.y - i) in everyWay:
				nearestWay = 'up'
				break;

		self.tower.setDirection(nearestWay)

	def getType(self):
		return self.type

	def render_underground(self):
		return self.sprite
	def render_tower(self):
		return self.tower.render()
	def render_deco(self):
		surf = pygame.Surface((32, 32), pygame.SRCALPHA)
		surf.blit(get_common().get_image('assets/level/tiles/Maptiles_0.png'), (0,0))
		surf.blit(self.sprite, (0,0))
		return surf


	def update(self, level):
		if self.tower!=None:
			self.tower.update(level, self.x, self.y)
		for enemy in self.enemies:
			enemy.update(level, self.x, self.y)
