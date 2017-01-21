import tower

class LightTower(tower.Tower):
	Cost=90
	name = "LIGHTWAVE TOWER"
	description = "Lumos Maxima! Blinds enemies with high\n concentrated power of will."
	effect_desc = ("Slows the target enemy by ", "[slow]", "%")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_DAMAGE
		self.EffectValue=10.5 # damage
		self.Speed=0.5 # in seconds
		self.setSprite('assets/level/towers/lighttower.png')
		self.setPlaceSound("assets/sound/light_tower/place.ogg")
		self.setAttackSound("assets/sound/light_tower/attack.ogg")
