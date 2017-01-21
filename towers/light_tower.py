import tower

class LightTower(tower.Tower):
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_SINGLE
		self.EffectValue=10 # percentage
		self.Speed=8.0 # in seconds
