# some constants
# effect types can be combined (e.g. to deal damage and stop enemies)
EFFECT_TYPE_NONE=0x0 # no effect at all
EFFECT_TYPE_DAMAGE=0x1 # tower will deal damage to one single opponent, EffectValue equals real damage
EFFECT_TYPE_SLOWDOWN=0x2 # slow down opponents, EffectValue equals percentage of slowdown (compared to enemy speed)
EFFECT_TYPE_STOP=0x4 # stop opponents' movement for a short time, EffectValue equals seconds to stop movement
EFFECT_TYPE_SINGLE=0x8 # single target on best field
EFFECT_TYPE_ALL=0x10 # all targets on best field
EFFECT_TYPE_CIRCLE=0x20 # all enemies in range
EFFECT_TYPE_STRAIGHT=0x40 # target only straight forward (obviously not together with circle^^)

class Tower:
	def __init__(self):
		self.EffectType=EFFECT_TYPE_NONE
		self.EffectMultiplier=1.0
		self.EffectValue=0
		self.Speed=10.0 # in seconds
		self.SpeedMultiplier=1.0
		self.Range=1 # one tile radius
		self.RangeMultiplier=1.0
