import tower

class BassTower(tower.Tower):
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_DAMAGE|tower.EFFECT_TYPE_CIRCLE
		self.EffectValue=1 # in real damage
		self.Speed=3 # in seconds
		self.setSprite('assets/level/towers/soundtower.png')
		self.Cost=90
		self.name = "SOUND TOWER"
		self.description = "As loud as Cannibal Corpse!"
		self.effect_desc = "Deals [damage] AoE damage"
		self.init()
