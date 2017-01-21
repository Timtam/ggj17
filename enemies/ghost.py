from random import randint
from enemy import Enemy

class Ghost(Enemy):
	def __init__(self, start):
		super(Ghost, self).__init__(start)
		self.health  = 100
		self.speed   = 0.5
		self.sound   = None
		self.setSprite("ghost")
		self.drop    = randint(1,3)
		