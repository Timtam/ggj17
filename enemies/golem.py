from random import randin
from enemy import Enemy

class Golem(Enemy):
	def __init__(self):
		super(Golem,self).__init__()
		self.health  = self.max_health = 900
		self.speed   = 3
		self.sound   = None
		self.damage  = 5
		self.setDieSound('assets/sound/boss/die.ogg')
		self.setSprite("golem")
		self.drop    = 72 + randint(-5, 5)
