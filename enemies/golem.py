class Golem(Enemy):
	def __init__(self):
		super(Golem,self).__init__()
		self.health  = 100
		self.speed   = 0.5
		self.sound   = None
		self.setSprite("golem")
		self.drop    = randint(1,3)