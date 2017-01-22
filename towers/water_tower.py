import tower

class WaterTower(tower.Tower):
	Cost=80
	name = "TSUNAMI TOWER"
	description = "Sends out Haitis Nightmare!"
	effect_desc = ("Slows one enemy in a line for ", "[stun]", "%")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=100 # percentage
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=0.1 #attc speed
		self.setSprite('watertower')
		self.setPlaceSound("assets/sound/water_tower/place.ogg")
		self.setAttackSound("assets/sound/water_tower/attack.ogg")
		self.set_animation('assets/level/towers/wave')
		self.animation_repeat = 2
		self.animation_speed = 5
		self.Range=16
