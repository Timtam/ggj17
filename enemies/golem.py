from random import randint
from enemy import Enemy

class Golem(Enemy):
	def __init__(self):
		super(Golem,self).__init__()
		self.health  = self.max_health = 1200
		self.speed   = 1.75
		self.damage  = 5
		self.setDieSound('assets/sound/boss/die.ogg')
		self.setArrivalSound("assets/sound/boss/arrival.ogg")
		self.setHitSound("assets/sound/boss/hit.ogg")
		self.setSprite("golem")
		self.drop    = 20 + randint(-5, 5)
