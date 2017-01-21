from random import randint
from enemy import Enemy

class Ghost(Enemy):
	def __init__(self):
		super(Ghost, self).__init__()
		self.health  = 100
		self.speed   = 0.1
		self.setDieSound("assets/sound/ghost/die.ogg")
		self.setSprite("ghost")
		self.drop    = randint(1,3)
