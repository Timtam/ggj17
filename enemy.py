from __future__ import division
import pygame
import time
from commons import *

DIRECTION_UP    = 0
DIRECTION_DOWN  = 1
DIRECTION_LEFT  = 2
DIRECTION_RIGHT = 3

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
		self.die = False

	def setSprite(self, filename):
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_up.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_down.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_left.png"))
		self.sprite.append(get_common().get_image("assets/level/enemies/" + filename + "_right.png"))

	def render(self):
		spriteHalfw = self.sprite[self.direction].get_width() / 2
		spriteHalfh = self.sprite[self.direction].get_height() / 2
		if self.direction == DIRECTION_RIGHT:
			return self.sprite[self.direction], ((-1) * spriteHalfw + ((time.time() - self.start) * 32 / self.speed) - 16 , 0)
		if self.direction == DIRECTION_LEFT:
			return self.sprite[self.direction], (spriteHalfw - ((time.time() - self.start) * 32 / self.speed) + 16, 0)
		if self.direction == DIRECTION_UP:
			return self.sprite[self.direction], (0, spriteHalfh - ((time.time() - self.start) * 32 / self.speed) + 16)
		if self.direction == DIRECTION_DOWN:
			return self.sprite[self.direction], (0, (-1) * spriteHalfh + ((time.time() - self.start) * 32 / self.speed) - 16)

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
		if self.die == True:
			# enemy is told to die, so do it, now!!!
			play_sound_fx(self.dieSound)
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])
			level.killed_enemies += 1
			return
		if (time.time() - self.start) > self.speed:
			index = level.level.index((x,y))
			if index == 0:
				level.current_lives -= self.damage
				self.addHealth(-self.getHealth()) # short for: die!!!
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
		if self.health <= 0:
			self.die = True
