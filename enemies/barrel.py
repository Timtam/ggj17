from random import randint
from enemy import Enemy

class Barrel(Enemy):
	def __init__(self):
		super(Barrel,self).__init__()
		self.health  = 75
		self.speed   = 0.75
		self.damage  = 1
		self.setDieSound('assets/sound/barrelguy/die.ogg')
		self.setSprite("barrel")
		self.drop    = 5 + randint(-2, 2)
