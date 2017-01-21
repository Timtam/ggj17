from random import randint
from enemy import Enemy

class Skeleton(Enemy):
	def __init__(self):
		super(Skelett,self).__init__()
		self.health  = 100
		self.speed   = 0.5
		self.sound   = None
		self.damage  = 1
		self.setDieSound('assets/sound/skeleton/die.ogg')
		self.setSprite("skeleton")
		self.drop    = randint(1,3)
