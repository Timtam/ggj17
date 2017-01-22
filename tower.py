from random import randint
import pygame
import math
import time
import os, os.path

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
		self.Sprite=[]
		self.PlaceSound=None
		self.AttackSound=None
		self.PendingTransaction=0
		self.LastFire=0
		self.EnemyCache = [] # saves all enemies which shouldn't be attacked again
		self.WillSell=False
		self.SellPercentage=50
		self.direction = 'up'
		self.animation = {}
		self.animation_data = {'index': 0, 'play': False, 'time': 0, 'direction': 'self', 'attacked_enemy': None}
		self.animation_repeat = 1
		self.animation_speed = 1

	def init(self):
		# setting PendingTransaction to the costs of the tower on first run, so the player needs to pay
		self.PendingTransaction=self.Cost
		play_sound_fx(self.PlaceSound)
		if self.EffectType & EFFECT_TYPE_CIRCLE == EFFECT_TYPE_CIRCLE:
			self.animation_data['direction'] = 'circle'
		elif self.EffectType & EFFECT_TYPE_STRAIGHT == EFFECT_TYPE_STRAIGHT:
			self.animation_data['direction'] = 'self'
		else:
			self.animation_data['direction'] = 'line'

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
					if (self.direction=="up" and (c_x!=x or c_y>=y)) or (self.direction=="right" and (c_x<=x or c_y!=y)) or (self.direction=="down" and (c_x!=x or c_y<=y)) or (self.direction=="left" and (c_x>=x or c_y!=y)):
						continue
				valid_targets.append((c_x, c_y, ))
		return valid_targets

	# needs all valid target fields as tuple array, as returned by find_target_fields
	# returns all actual targets (deal damage here) as tuple-array
	def filter_target_fields(self, level, valid_targets):
		enemies=[]
		j=0
		nearest_field=None
		targets=[]
		i=0
		# filter all fields without enemies
		for i in range(len(valid_targets)):
			enemies=[]
			if level.grid[valid_targets[i][0]][valid_targets[i][1]].getType()!=1:
				continue
			for j in range(len(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies)):
				if self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN and level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies[j] in self.EnemyCache:
					continue
				enemies.append(level.grid[valid_targets[i][0]][valid_targets[i][1]].enemies[j])
			if len(enemies)==0:
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

	def setDirection(self, nearestWay):
		self.direction = nearestWay

	def update(self,level,x,y):
		enemy=None
		enemies=[]
		i=0
		j=0
		# to pay the crystals required
		if self.WillSell==True:
			level.grid[x][y].tower=None
			level.cash+=self.Cost*self.SellPercentage/100
			self.WillSell=False
			return
		if self.PendingTransaction>0:
			if self.PendingTransaction>level.cash:
				raise IOError("User wants to build tower, but doesn't have enough money. Please try again later!")
			level.cash=level.cash-self.PendingTransaction
			self.PendingTransaction=0
		valid_targets = self.find_target_fields(level.grid,x,y)
		valid_targets=self.filter_target_fields(level, valid_targets)
		if self.animation_data['play']:
			anim_fraction = (time.time() - self.LastFire) / (self.SpeedMultiplier * self.Speed) * self.animation_speed
			if anim_fraction >= 1:
				self.animation_data['play'] = False
				self.animation_data['index'] = 0
			elif len(self.animation) > 0:
				self.animation_data['index'] = int(math.floor(len(self.animation.values()[0]) * ((anim_fraction * self.animation_repeat) %  1)))
			if self.animation_data['attacked_enemy'] != None:
				self.animation_data['attacked_enemy_coords'] = self.animation_data['attacked_enemy'].coords
				self.animation_data['enemy_field_relative'] = (self.animation_data['attacked_enemy'].field[0] - x, self.animation_data['attacked_enemy'].field[1] - y)
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
						enemy.speedMultiplier+=self.EffectValue*enemy.speedMultiplier/100.0
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
				self.animation_data['attacked_enemy'] = enemy
				self.animation_data['attacked_enemy_coords'] = enemy.coords
				self.animation_data['enemy_field_relative'] = (valid_targets[i][0] - x, valid_targets[i][1] - y)
				if self.EffectType&EFFECT_TYPE_DAMAGE==EFFECT_TYPE_DAMAGE:
					enemy.addHealth(-(self.EffectMultiplier*self.EffectValue))
				elif self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN:
					enemy.speedMultiplier+=self.EffectValue*enemy.speedMultiplier/100.0
					self.EnemyCache.append(enemy)
			play_sound_fx(self.AttackSound)
			self.LastFire=time.time()
			self.animation_data['play'] = True

	def setSprite(self, path):
		self.Sprite.append(get_common().get_image("assets/level/towers/" + path + "_up.png"))
		self.Sprite.append(get_common().get_image("assets/level/towers/" + path + "_down.png"))
		self.Sprite.append(get_common().get_image("assets/level/towers/" + path + "_left.png"))
		self.Sprite.append(get_common().get_image("assets/level/towers/" + path + "_right.png"))

	def setPlaceSound(self,filename):
		self.PlaceSound=filename

	def setAttackSound(self, filename):
		self.AttackSound = filename

	def set_animation(self, path):
		animation_name = path[(path.rfind('/') + 1):] + '_'
		for direction in ('left', 'right', 'up', 'down', 'circle', 'line'):
			dir_path = path + '_' + direction + '/'
			base_file_name = animation_name + direction + '_'
			if os.path.exists(dir_path):
				self.animation[direction] = []
				self.animation_data[direction] = {'index': 0, 'time': time.time()}
				files = [f for f in os.listdir(dir_path) if os.path.isfile(dir_path + f) and f.startswith(base_file_name)]
				files.sort()
				for f in files:
					self.animation[direction].append(get_common().get_image(dir_path + f))

	def render(self):
		if self.direction == 'up':
			return self.Sprite[0]
		if self.direction == 'down':
			return self.Sprite[1]
		if self.direction == 'left':
			return self.Sprite[2]
		if self.direction == 'right':
			return self.Sprite[3]

	def render_animation(self):
		anim_direction = self.animation_data['direction']
		if anim_direction == 'self':
			anim_direction = self.direction
		if anim_direction not in self.animation or not self.animation_data['play']:
			return pygame.Surface((0, 0), pygame.SRCALPHA), (0, 0), False

		animation = self.animation[anim_direction]
		surf = animation[self.animation_data['index']]
		render_above = False
		if anim_direction == 'up':
			coords = ((32 - surf.get_width()) / 2, -surf.get_height())
		elif anim_direction == 'down':
			coords = ((32 - surf.get_width()) / 2, 32)
		elif anim_direction == 'left':
			surf = pygame.transform.scale(surf, (int(32 * self.Range * self.RangeMultiplier), 32))
			coords = (-surf.get_width(), (32 - surf.get_height()) / 2)
		elif anim_direction == 'right':
			surf = pygame.transform.scale(surf, (int(32 * self.Range * self.RangeMultiplier), 32))
			coords = (32, (32 - surf.get_height()) / 2)
		elif anim_direction == 'circle':
			surf = pygame.transform.scale(surf, (32 + int(64 * self.Range * self.RangeMultiplier), 32 + int(64 * self.Range * self.RangeMultiplier)))
			coords = ((32 - surf.get_width()) / 2, (32 - surf.get_height()) / 2)
		elif anim_direction == 'line':
			enemy_coords = self.animation_data['attacked_enemy_coords']
			field = self.animation_data['enemy_field_relative']
			sprite = self.render()
			tower_source = (16, 32 - sprite.get_height() + 16)
			target_coords = (field[0] * 32 + enemy_coords[0] + 16, field[1] * 32 + enemy_coords[1] + 16)
			angle = (-math.atan2(target_coords[1] - tower_source[1], target_coords[0] - tower_source[0])) / math.pi * 180
			length = math.hypot(target_coords[0] - tower_source[0], target_coords[1] - tower_source[1])
			surf = pygame.transform.scale(surf, (int(length), surf.get_height()))
			surf = pygame.transform.rotate(surf, angle)
			coords = (min(target_coords[0], tower_source[0]), min(target_coords[1], tower_source[1]))
			render_above = (target_coords[1] > 0)
		return surf, coords, render_above

	def Sell(self):
		self.WillSell=True
