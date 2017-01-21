from random import randint
from enemy import Enemy

class Barrel(Enemy):
	def __init__(self):
		super(Barrel,self).__init__()
		self.health  = 100
		self.speed   = 0.5
		self.sound   = None
		self.damage  = 1
		self.setDieSound('assets/sound/barrelguy/die.ogg')
		self.setSprite("barrel")
		self.drop    = randint(1,3)
