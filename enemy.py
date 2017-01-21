import pygame
import timeit

DIRECTION_UP    = 0
DIRECTION_DOWN  = 1
DIRECTION_LEFT  = 2
DIRECTION_RIGHT = 3

class Enemy(object):
	def __init__(self, start):
		self.health    = None
		self.speed     = None
		self.sound     = None
		self.sprite    = []
		self.drop      = None
		self.direction = DIRECTION_RIGHT
		self.start     = start
		
	def setSprite(self, filename):
		self.sprite.append(pygame.image.load("assets/level/enemies/" + filename + "_up.png"))
		self.sprite.append(pygame.image.load("assets/level/enemies/" + filename + "_down.png"))
		self.sprite.append(pygame.image.load("assets/level/enemies/" + filename + "_left.png"))
		self.sprite.append(pygame.image.load("assets/level/enemies/" + filename + "_right.png"))
		
	def render(self):
		return self.sprite[self.direction]
	
	def setDirection(self, direction):
		self.direction = direction
		
	def getHealth(self):
		return self.health
	
	def getSpeed(self):
		return self.health
		
	def getSound(self):
		return self.sound
		
	def getDrop(self):
		return self.drop
	
	def setStart(self, start):
		self.start = start
	
	def update(self, level, x, y):
		if (timeit.default_timer() - self.start) > self.speed:
			index = level.level.index((x,y))
			print index
			#TODO index == 0: Enemy am Ende der Karte => Schaden fuer Spieler
			next = level.level[index-1]
			print next
			field = level.grid[next[0]][next[1]]
			self.setStart(timeit.default_timer())
			field.enemies.append(self)
			del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])
			print "wechsel"