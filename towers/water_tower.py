import tower

class WaterTower(tower.Tower):
	Cost=140
	name = "TSUNAMI TOWER"
	description = "Sends out Haitis Nightmare!"
	effect_desc = ("Stuns a couple of enemies in a line for ", "[stun]", "s")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=20 # percentage
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=5
		self.setSprite('assets/level/towers/watertower.png')
		self.setPlaceSound("assets/sound/water_tower/place.ogg")
		self.setAttackSound("assets/sound/water_tower/attack.ogg")
