import tower

class LightTower(tower.Tower):
	Cost=80
	name = "LIGHTWAVE TOWER"
	description = "Lumos Maxima! Blinds enemies with high\n concentrated power of will."
	effect_desc = ("Slows the target enemy by ", "[slow]", "%")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_SLOWDOWN|tower.EFFECT_TYPE_SINGLE
		self.EffectValue=10 # percentage
		self.Speed=8.0 # in seconds
		self.setSprite('assets/level/towers/lighttower.png')
		self.setPlaceSound("assets/sound/light_tower/place.ogg")
