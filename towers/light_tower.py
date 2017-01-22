import tower

class LightTower(tower.Tower):
	Cost=90
	name = "LIGHTWAVE TOWER"
	description = "Lumos Maxima! Deals damage to single targets with high\n concentrated power of will."
	effect_desc = ("Deals damage to the target enemy by ", "[slow]", "dps")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_DAMAGE
		self.EffectValue=10.5 # damage
		self.Speed=0.5 # in seconds
		self.setSprite('lighttower')
		self.setPlaceSound("assets/sound/light_tower/place.ogg")
		self.setAttackSound("assets/sound/light_tower/attack.ogg")
		self.set_animation('assets/level/towers/light')
		self.animation_speed = 4
