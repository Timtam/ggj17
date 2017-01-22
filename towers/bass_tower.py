import tower

class BassTower(tower.Tower):
	Cost=100
	name = "SOUND TOWER"
	description = "As loud as Cannibal Corpse!"
	effect_desc = ("Deals ", "[damage]", " AoE damage")
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectType=tower.EFFECT_TYPE_DAMAGE|tower.EFFECT_TYPE_CIRCLE|tower.EFFECT_TYPE_ALL
		self.EffectValue= 8.0 # in real damage
		self.Speed=1 # in seconds
		self.setSprite('soundtower')
		self.setPlaceSound("assets/sound/sound_tower/place.ogg")
		self.setAttackSound("assets/sound/sound_tower/attack.ogg")
		self.set_animation('assets/level/towers/bass')
		self.setUpgradeSound("assets/sound/sound_tower/upgrade.ogg")

		self.SetUpgradeCost(tower.UPGRADE_SPEED, 70)
		self.SetUpgradeMultiplier(tower.UPGRADE_SPEED, 0.7)

		self.SetUpgradeCost(tower.UPGRADE_EFFECT, 80)
		self.SetUpgradeMultiplier(tower.UPGRADE_EFFECT, 1.5)

		self.SetUpgradeCost(tower.UPGRADE_RANGE, 100)
		self.SetUpgradeMultiplier(tower.UPGRADE_RANGE, 2.0)

	def onUpgrade(self, upgrade):
		if upgrade == tower.UPGRADE_EFFECT:
			self.setAttackSound("assets/sound/sound_tower/attack_upgrade.ogg")
			self.setImpact("golem", 0.75)
			self.setImpact("barrel", 0.8)
