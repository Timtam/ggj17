from __future__ import division
import pygame
import time
from commons import *

DIRECTION_UP    = 0
DIRECTION_DOWN  = 1
DIRECTION_LEFT  = 2
DIRECTION_RIGHT = 3

DIE_DAMAGE=1
DIE_SUCCESS=2

class Enemy(object):
	def __init__(self):
		self.health    = None
		self.speed     = None
		self.dieSound  = None
		self.speedMultiplier = 1.0
		self.arrivalSound = None
		self.hitSound = "assets/sound/common/hit.ogg"
		self.sprite    = []
		self.drop      = None
		self.damage    = 1 # damage done to player's castle
		self.direction = DIRECTION_RIGHT
		self.start     = time.time()
		self.die = 0
		self.health_empty = get_common().get_image('assets/ui/health_empty.png')
		self.health_full = get_common().get_image('assets/ui/health_full.png')
		self.coords = (0, 0)
		self.field = (0, 0)
		self.name = ""

	def init(self):
		if self.arrivalSound!=None:
			play_sound_fx(self.arrivalSound)

	def setSprite(self, filename):
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_up.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_down.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_left.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_right.png"))

	def render(self):
		spriteHalfw = self.sprite[self.direction].get_width() / 2
		spriteHalfh = self.sprite[self.direction].get_height() / 2
		sprite = self.sprite[self.direction]
		coords = (self.coords[0], self.coords[1] - 5)
		surf = pygame.Surface((sprite.get_width(), sprite.get_height() + 5), pygame.SRCALPHA)
		surf.blit(sprite, (0, 5))
		surf.blit(self.health_empty, (spriteHalfw - 16, 0))
		health_fract = max(0, self.health / self.max_health)
		health_full = pygame.Surface((int(health_fract * 30), 2), pygame.SRCALPHA)
		if health_fract > 0.5:
			health_full.fill(pygame.Color(0, 170, 0, 255))
		elif health_fract > 0.25:
			health_full.fill(pygame.Color(200, 200, 0, 255))
		else:
			health_full.fill(pygame.Color(255, 0, 0, 255))
		surf.blit(health_full, (spriteHalfw - 15, 1))
		return surf, coords

	def setDirection(self, direction):
		self.direction = direction

	def getHealth(self):
		return self.health

	def getSpeed(self):
		return (self.speed * self.speedMultiplier)

	def getDieSound(self):
		return self.dieSound

	def setDieSound(self, filename):
		self.dieSound = filename

	def setArrivalSound(self, filename):
		self.arrivalSound = filename

	def setHitSound(self, filename):
		self.hitSound = filename

	def getDrop(self):
		return self.drop

	def setStart(self, start):
		self.start = start

	def update(self, level, x, y):
		if self.die>0:
			# enemy is told to die, so do it, now!!!
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])
			level.remove_enemy(self)
			if self.die==DIE_DAMAGE:
				play_sound_fx("assets/sound/common/coin.ogg")
			elif self.die==DIE_SUCCESS:
				play_sound_fx(self.hitSound)
			return
		self.field = (x, y)

		newfield = False

		if (time.time() - self.start) > (self.speed * self.speedMultiplier):
			index = level.level.index((x,y))
			if index == 0:
				self.die = DIE_SUCCESS
				return

			next = level.level[index-1]
			#x bleibt gleich und y erhoeht sich => Nach unten
			if x == next[0] and y < next[1]:
				self.setDirection(DIRECTION_DOWN)
			#x bleibt gleich und y wird kleiner => Nach oben
			if x == next[0] and y > next[1]:
				self.setDirection(DIRECTION_UP)
			#y bleibt gleich und x wird kleiner => Nach links
			if y == next[1] and x < next[0]:
				self.setDirection(DIRECTION_RIGHT)
			if y == next[1] and x > next[0]:
				self.setDirection(DIRECTION_LEFT)

			self.field = (next[0], next[1])
			field = level.grid[next[0]][next[1]]
			self.setStart(time.time())
			self.corner = False
			field.enemies.append(self)
			newfield = True
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])

		# update render coords
		spriteHalfw = self.sprite[self.direction].get_width() / 2
		spriteHalfh = self.sprite[self.direction].get_height() / 2
		oldCoords = self.coords
		if self.direction == DIRECTION_RIGHT:
			self.coords = ((-1) * spriteHalfw + ((time.time() - self.start) * 32 / (self.speed * self.speedMultiplier)) - 16 , 0)
			if oldCoords[0] > self.coords[0] and newfield:
				self.coord = oldCoords
		elif self.direction == DIRECTION_LEFT:
			self.coords = (spriteHalfw - ((time.time() - self.start) * 32 / (self.speed * self.speedMultiplier)) + 16, 0)
			if oldCoords[0] < self.coords[0] and newfield:
				self.coord = oldCoords
		elif self.direction == DIRECTION_UP:
			self.coords = (0, spriteHalfh - ((time.time() - self.start) * 32 / (self.speed * self.speedMultiplier)) + 16)
			if oldCoords[1] > self.coords[1] and newfield:
				self.coord = oldCoords
		elif self.direction == DIRECTION_DOWN:
			self.coords = (0, (-1) * spriteHalfh + ((time.time() - self.start) * 32 / (self.speed * self.speedMultiplier)) - 16)
			if oldCoords[0] < self.coords[0] and newfield:
				self.coord = oldCoords

	def addHealth(self, health):
		self.health += health
		if self.health <= 0:
			self.die = DIE_DAMAGE
			play_sound_fx(self.dieSound)
