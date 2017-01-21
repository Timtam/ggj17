import tower

class WaterTower(tower.Tower):
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=0.3 # in seconds
		self.EffectType=tower.EFFECT_TYPE_STOP|tower.EFFECT_TYPE_ALL|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=12
		self.setSprite('assets/level/towers/watertower.png')
		self.Cost=140
		self.name = "TSUNAMI TOWER"
		self.description = "Sends out Haitis Nightmare!"
		self.effect_desc = "Stuns a coupls of enemies in a line for [stun]s"
		self.init()
