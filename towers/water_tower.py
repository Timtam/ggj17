import tower

class WaterTower(tower.Tower):
	Cost=140
	name = "TSUNAMI TOWER"
	description = "Sends out Haitis Nightmare!"
	effect_desc = ("Stuns a couple of enemies in a line for ", "[stun]", "s")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=0.3 # in seconds
		self.EffectType=tower.EFFECT_TYPE_STOP|tower.EFFECT_TYPE_ALL|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=12
		self.setSprite('assets/level/towers/watertower.png')
		self.setPlaceSound("assets/sound/water_tower/place.ogg")
