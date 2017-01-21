from random import randin
from enemy import Enemy

class Golem(Enemy):
	def __init__(self):
		super(Golem,self).__init__()
		self.health  = 100
		self.speed   = 0.5
		self.sound   = None
		self.damage  = 5
		self.setDieSound('assets/sound/boss/die.ogg')
		self.setSprite("golem")
		self.drop    = randint(1,3)
