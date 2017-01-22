import tower

class WaterTower(tower.Tower):
	Cost=120
	name = "TSUNAMI TOWER"
	description = "Sends out Haitis Nightmare!"
	effect_desc = ("Slows a couple of enemies in a line for ", "[stun]", "s")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=40 # percentage
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=5 #attc speed
		self.setSprite('watertower')
		self.setPlaceSound("assets/sound/water_tower/place.ogg")
		self.setAttackSound("assets/sound/water_tower/attack.ogg")
		self.Range=16
