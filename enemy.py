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
		self.sprite    = []
		self.drop      = None
		self.damage    = None # damage done to player's castle
		self.direction = DIRECTION_RIGHT
		self.start     = time.time()
		self.die = 0
		self.health_empty = get_common().get_image('assets/ui/health_empty.png')
		self.health_full = get_common().get_image('assets/ui/health_full.png')

	def setSprite(self, filename):
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_up.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_down.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_left.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_right.png"))

	def render(self):
		spriteHalfw = self.sprite[self.direction].get_width() / 2
		spriteHalfh = self.sprite[self.direction].get_height() / 2
		if self.direction == DIRECTION_RIGHT:
			coords = ((-1) * spriteHalfw + ((time.time() - self.start) * 32 / self.speed) - 16 , 0)
		if self.direction == DIRECTION_LEFT:
			coords = (spriteHalfw - ((time.time() - self.start) * 32 / self.speed) + 16, 0)
		if self.direction == DIRECTION_UP:
			coords = (0, spriteHalfh - ((time.time() - self.start) * 32 / self.speed) + 16)
		if self.direction == DIRECTION_DOWN:
			coords = (0, (-1) * spriteHalfh + ((time.time() - self.start) * 32 / self.speed) - 16)

		sprite = self.sprite[self.direction]
		coords = (coords[0], coords[1] - 5)
		surf = pygame.Surface((sprite.get_width(), sprite.get_height() + 5), pygame.SRCALPHA)
		surf.blit(sprite, (0, 5))
		surf.blit(self.health_empty, (spriteHalfw - 16, 0))
		surf.blit(self.health_full, (spriteHalfw - 15, 1), pygame.Rect(0, 0, int(self.health / self.max_health * 30), 2))
		return surf, coords

	def setDirection(self, direction):
		self.direction = direction

	def getHealth(self):
		return self.health

	def getSpeed(self):
		return self.speed

	def getDieSound(self):
		return self.dieSound

	def setDieSound(self, filename):
		self.dieSound = filename

	def getDrop(self):
		return self.drop

	def setStart(self, start):
		self.start = start

	def update(self, level, x, y):
		if self.die>0:
			# enemy is told to die, so do it, now!!!
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])
			if self.die==DIE_DAMAGE:
				level.killed_enemies += 1
				level.cash += self.drop
			return
		if (time.time() - self.start) > self.speed:
			index = level.level.index((x,y))
			if index == 0:
				level.current_lives -= self.damage
				self.die = DIE_SUCCESS
				# TODO: check in level if game over or not and end if yes (maybe outside of update?)
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

			field = level.grid[next[0]][next[1]]
			self.setStart(time.time())
			self.corner = False
			field.enemies.append(self)
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])

	def addHealth(self, health):
		self.health += health
		print "remaining: %f"%self.health
		if self.health <= 0:
			self.die = DIE_DAMAGE
			play_sound_fx(self.dieSound)
