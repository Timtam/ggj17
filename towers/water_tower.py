import tower

class WaterTower(tower.Tower):
	Cost=140
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=0.3 # in seconds
		self.EffectType=tower.EFFECT_TYPE_STOP|tower.EFFECT_TYPE_ALL|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=12
		self.setSprite('assets/level/towers/watertower.png')
		self.sedtPlaceSound("assets/sound/water_tower/place.ogg")
