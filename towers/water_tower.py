import tower

class WaterTower(tower.Tower):
	Cost=80
	name = "TSUNAMI TOWER"
	description = "Sends out Haitis Nightmare!"
	effect_desc = ("Slows one enemy in a line for ", "[stun]", "%")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=60 # percentage
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=0.5 #attc speed
		self.setSprite('watertower')
		self.setPlaceSound("assets/sound/water_tower/place.ogg")
		self.setAttackSound("assets/sound/water_tower/attack.ogg")
		self.set_animation('assets/level/towers/wave', 2, 5)
		self.animation_repeat = 1
		self.animation_speed = 1
		self.animation_scale = tower.ANIMATION_SCALE_TRANSLATE
		self.Range=16
