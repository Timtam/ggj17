from random import randint
from enemy import Enemy

class Ghost(Enemy):
	def __init__(self):
		super(Ghost, self).__init__()
		self.health  = self.max_health = 150
		self.speed   = 0.75
		self.setDieSound("assets/sound/ghost/die.ogg")
		self.setSprite("ghost")
		self.drop    = 7 + randint(-2, 2)
		self.name = "ghost"