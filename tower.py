import pygame
import math

from commons import *

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
		self.Sprite=None
		self.Cost=0
		self.PendingTransaction=0

	def init(self):
		# setting PendingTransaction to the costs of the tower on first run, so the player needs to pay
		self.PendingTransaction=self.Cost

	# finds all valid target fields
	def find_target_fields(self, fields, x, y):
		c_x=0
		c_y=0
		i_x1=x-(int(self.Range*self.RangeMultiplier))
		i_x2=x+(int(self.Range*self.RangeMultiplier))
		i_y1=y-(int(self.Range*self.RangeMultiplier))
		i_y2=y+(int(self.Range*self.RangeMultiplier))
		if i_x1<0:
			i_x1=0
		if i_x2>=len(fields):
			i_x2=len(fields)-1
		if i_y1<0:
			i_y1=0
		if i_y2>=len(fields[0]):
			i_y2=len(fields[0])-1
		valid_targets = [] # contains x and y tuples
		if math.floor(self.Range*self.RangeMultiplier)!=self.Range*self.RangeMultiplier:
			raise IOError("Range * RangeMultiplier = %f, but only integers allowed"%(self.Range*self.RangeMultiplier))
		for c_x in range(i_x1,i_x2+1):
			for c_y in range(i_y1, i_y2+1):
				if c_x==x and c_y==y:
					continue
				if self.EffectType&EFFECT_TYPE_STRAIGHT==EFFECT_TYPE_STRAIGHT:
					if c_x!=x and c_y!=y:
						continue
				valid_targets.append((c_x, c_y, ))
		return valid_targets

	# needs all valid target fields as tuple array, as returned by find_target_fields
	# returns all actual targets (deal damage here) as tuple-array
	def filter_target_fields(self, level, valid_targets):
		nearest_field=None
		targets=[]
		i=0
		# filter all fields without enemies
		for i in range(len(valid_targets)):
			if level.grid[valid_targets[i][0]][valid_targets[i][1]].getType()!=1:
				continue
			if len(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies)==0:
				continue
			targets.append(valid_targets[i])
		# no targets left?
		if len(targets)==0:
			return []
		if self.EffectType&EFFECT_TYPE_CIRCLE!=EFFECT_TYPE_CIRCLE:
			# filtering down to just one valid field, only one field should be attacked
			# per definition (Henry) this should be the field with the lowest distance to the target
			nearest_field=targets[0]
			for i in range(1,len(targets)):
				if level.level.index((targets[i][0], targets[i][1], ))<level.level.index((nearest_field[0], nearest_field[1], )):
					nearest_field=targets[i]
			targets=[nearest_field]
		return targets

	def update(self,level,x,y):
		# to pay the crystals required
		if self.PendingTransaction>0:
			if self.PendingTransaction>level.cash:
				raise IOError("User wants to build tower, but doesn't have enough money. Please try again later!")
			level.cash=level.cash-self.PendingTransaction
			self.PendingTransaction=0
		valid_targets = self.find_target_fields(level.grid,x,y)
		valid_targets=self.filter_target_fields(level, valid_targets)

	def setSprite(self, path):
		self.Sprite = get_common().get_image(path)

	def render(self):
		return self.Sprite
