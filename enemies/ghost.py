from random import randint
from enemy import Enemy

class Ghost(Enemy):
	def __init__(self):
		super(Ghost, self).__init__()
		self.health  = self.max_health = 100
		self.speed   = 1.0
		self.setDieSound("assets/sound/ghost/die.ogg")
		self.setSprite("ghost")
		self.drop    = 5 + randint(-2, 2)
