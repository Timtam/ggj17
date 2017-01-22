from random import randint
from enemy import Enemy

class Skeleton(Enemy):
	def __init__(self):
		super(Skeleton,self).__init__()
		self.health  = self.max_health = 175
		self.speed   = 1.25
		self.setDieSound('assets/sound/skeleton/die.ogg')
		self.setSprite("skeleton")
		self.drop    = 9 + randint(-2, 2)
		self.name = "skeleton"
