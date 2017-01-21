import tower

class BassTower(tower.Tower):
	Cost=90
	name = "SOUND TOWER"
	description = "As loud as Cannibal Corpse!"
	effect_desc = ("Deals ", "[damage]", " AoE damage")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_DAMAGE|tower.EFFECT_TYPE_CIRCLE|tower.EFFECT_TYPE_ALL
		self.EffectValue=5.0 # in real damage
		self.Speed=2.0 # in seconds
		self.setSprite('assets/level/towers/soundtower.png')
		self.setPlaceSound("assets/sound/sound_tower/place.ogg")
		self.setAttackSound("assets/sound/sound_tower/attack.ogg")
