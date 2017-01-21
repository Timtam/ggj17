from random import randint
from enemy import Enemy

class Skeleton(Enemy):
	def __init__(self):
		super(Skeleton,self).__init__()
		self.health  = self.max_health = 125
		self.speed   = 1.25
		self.sound   = None
		self.damage  = 1
		self.setDieSound('assets/sound/skeleton/die.ogg')
		self.setSprite("skeleton")
		self.drop    = 10 + randint(-2, 2)
