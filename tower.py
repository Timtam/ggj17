from random import randint
import pygame
import math
import time

from commons import *

# some constants
# effect types can be combined (e.g. to deal damage and stop enemies)
EFFECT_TYPE_NONE=0x0 # no effect at all
EFFECT_TYPE_DAMAGE=0x1 # tower will deal damage to one single opponent, EffectValue equals real damage
EFFECT_TYPE_SLOWDOWN=0x2 # slow down opponents, EffectValue equals percentage of slowdown (compared to enemy speed)
EFFECT_TYPE_ALL=0x4 # all targets on best field
EFFECT_TYPE_CIRCLE=0x8 # all enemies in range
EFFECT_TYPE_STRAIGHT=0x10 # target only straight forward (obviously not together with circle^^)

class Tower:
	Cost=0
	def __init__(self):
		self.EffectType=EFFECT_TYPE_NONE
		self.EffectMultiplier=1.0
		self.EffectValue=0
		self.Speed=10.0 # in seconds
		self.SpeedMultiplier=1.0
		self.Range=1 # one tile radius
		self.RangeMultiplier=1.0
		self.Sprite=None
		self.PlaceSound=None
		self.AttackSound=None
		self.PendingTransaction=0
		self.LastFire=0
		self.EnemyCache = [] # saves all enemies which shouldn't be attacked again

	def init(self):
		# setting PendingTransaction to the costs of the tower on first run, so the player needs to pay
		self.PendingTransaction=self.Cost
		play_sound_fx(self.PlaceSound)

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
		enemy=None
		enemies=[]
		i=0
		j=0
		# to pay the crystals required
		if self.PendingTransaction>0:
			if self.PendingTransaction>level.cash:
				raise IOError("User wants to build tower, but doesn't have enough money. Please try again later!")
			level.cash=level.cash-self.PendingTransaction
			self.PendingTransaction=0
		valid_targets = self.find_target_fields(level.grid,x,y)
		valid_targets=self.filter_target_fields(level, valid_targets)
		if len(valid_targets)==0:
			return
		if time.time()-self.LastFire<(self.SpeedMultiplier*self.Speed):
			return
		for i in range(len(valid_targets)):
			if self.EffectType&EFFECT_TYPE_ALL==EFFECT_TYPE_ALL:
				for j in range(len(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies)):
					enemy=level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies[j]
					if self.EffectType&EFFECT_TYPE_DAMAGE==EFFECT_TYPE_DAMAGE:
						enemy.addHealth(-(self.EffectMultiplier*self.EffectValue))
					elif self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN:
						if enemy in self.EnemyCache:
							continue
						enemy.speedMultiplier-=self.EffectValue*enemy.speedMultiplier/100.0
						self.EnemyCache.append(enemy)
			else:
				enemies=[]
				for j in range(len(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies)):
					if self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN and level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies[j] in self.EnemyCache:
						continue
					enemies.append(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies[j])
				if len(enemies)==0:
					return
				enemy=enemies[randint(0,len(enemies)-1)]
				if self.EffectType&EFFECT_TYPE_DAMAGE==EFFECT_TYPE_DAMAGE:
					enemy.addHealth(-(self.EffectMultiplier*self.EffectValue))
				elif self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN:
					enemy.speedMultiplier-=self.EffectValue*enemy.speedMultiplier/100.0
			play_sound_fx(self.AttackSound)
			self.LastFire=time.time()

	def setSprite(self, path):
		self.Sprite = get_common().get_image(path)

	def setPlaceSound(self,filename):
		self.PlaceSound=filename

	def setAttackSound(self, filename):
		self.AttackSound = filename

	def render(self):
		return self.Sprite
