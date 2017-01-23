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

ANIMATION_SCALE_SCALE = 1 # scale animation to correct size
ANIMATION_SCALE_TRANSLATE = 2 # move animation from start to end instead of scaling

UPGRADE_SPEED = 0
UPGRADE_EFFECT = 1
UPGRADE_RANGE=2

UPGRADE_FALSE = 0
UPGRADE_PENDING = 1
UPGRADE_TRUE = 2

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
        self.SellPercentageUpgrades = 30
        self.UpgradeCosts=[0,0,0]
        self.UpgradeMultipliers=[0.0,0.0,0.0]
        self.UpgradeStatus=[UPGRADE_FALSE,UPGRADE_FALSE,UPGRADE_FALSE]
        self.UpgradeSound = None
        self.Impacts={}
        self.direction = 'up'
        self.animation = {}
        self.animation_data = {'index': 0, 'fraction': 0, 'play': False, 'time': 0, 'direction': 'self', 'attacked_enemy': None}
        self.animation_repeat = 1
        self.animation_speed = 1
        self.animation_scale = ANIMATION_SCALE_SCALE

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
        if self.WillSell==True:
            level.grid[x][y].tower=None
            level.cash+=self.getValue()
            self.WillSell=False
            play_sound_fx("assets/sound/common/sell.ogg")
            play_sound_fx("assets/sound/common/coin.ogg")
            return
        for i in range(len(self.UpgradeStatus)):
            if self.UpgradeStatus[i]==UPGRADE_PENDING:
                self.PendingTransaction=self.UpgradeCosts[i]
                self.UpgradeStatus[i]=UPGRADE_TRUE
                if i == UPGRADE_SPEED:
                    self.SpeedMultiplier=self.UpgradeMultipliers[i]
                elif i == UPGRADE_RANGE:
                    self.RangeMultiplier=self.UpgradeMultipliers[i]
                elif i == UPGRADE_EFFECT:
                    self.EffectMultiplier=self.UpgradeMultipliers[i]
                play_sound_fx(self.UpgradeSound)
                self.onUpgrade(i)
                break
        # to pay the crystals required
        if self.PendingTransaction>0:
            if self.PendingTransaction>level.cash:
                raise IOError("User wants to build or upgrade tower, but doesn't have enough money. Please try again later!")
            level.cash-=self.PendingTransaction
            self.PendingTransaction=0
        valid_targets = self.find_target_fields(level.grid,x,y)
        valid_targets=self.filter_target_fields(level, valid_targets)
        if self.animation_data['play']:
            anim_fraction = (time.time() - self.LastFire) / (self.SpeedMultiplier * self.Speed) * self.animation_speed
            if anim_fraction >= 1:
                self.animation_data['play'] = False
                self.animation_data['index'] = 0
                self.animation_data['fraction'] = 0
            elif len(self.animation) > 0:
                self.animation_data['fraction'] = (anim_fraction * self.animation_repeat) %  1
                self.animation_data['index'] = int(math.floor(len(self.animation.values()[0]) * self.animation_data['fraction']))
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
                        enemy.addHealth(-self.getImpact(enemy.name)*(self.EffectMultiplier*self.EffectValue))
                    elif self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN:
                        if enemy in self.EnemyCache:
                            continue
                        enemy.speedMultiplier+=self.getImpact(enemy.name)*(self.EffectValue*enemy.speedMultiplier/100.0)
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
                    enemy.addHealth(-self.getImpact(enemy.name)*(self.EffectMultiplier*self.EffectValue))
                elif self.EffectType&EFFECT_TYPE_SLOWDOWN==EFFECT_TYPE_SLOWDOWN:
                    enemy.speedMultiplier+=self.getImpact(enemy.name)*(self.EffectValue*enemy.speedMultiplier/100.0)
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

    def set_animation(self, path, repeat_frames = 0, repeat_count = 0):
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
                for i in range(repeat_count * repeat_frames):
                    self.animation[direction].append(self.animation[direction][-repeat_frames])

    def render(self):
        surf = pygame.Surface(self.Sprite[0].get_rect().size, pygame.SRCALPHA)

        if self.direction == 'up':
            surf.blit(self.Sprite[0], (0,0))
        if self.direction == 'down':
            surf.blit(self.Sprite[1], (0,0))
        if self.direction == 'left':
            surf.blit(self.Sprite[2], (0,0))
        if self.direction == 'right':
            surf.blit(self.Sprite[3], (0,0))

        if self.UpgradeStatus[0] == 2:
            surf.blit(get_common().get_image("assets/level/towers/upgrade_effect.png"), (2, 10))
        if self.UpgradeStatus[1] == 2:
            surf.blit(get_common().get_image("assets/level/towers/upgrade_range.png"), (2, 20))
        if self.UpgradeStatus[2] == 2:
            surf.blit(get_common().get_image("assets/level/towers/upgrade_speed.png"), (2, 30))

        return surf

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
            if self.animation_scale == ANIMATION_SCALE_SCALE:
                surf = pygame.transform.scale(surf, (32, int(32 * self.Range * self.RangeMultiplier)))
                coords = ((32 - surf.get_width()) / 2, -surf.get_height())
            else:
                coords = ((32 - surf.get_width()) / 2, -surf.get_height() - self.animation_data['fraction'] * 32 * (self.Range * self.RangeMultiplier - 1))
        elif anim_direction == 'down':
            if self.animation_scale == ANIMATION_SCALE_SCALE:
                surf = pygame.transform.scale(surf, (32, int(32 * self.Range * self.RangeMultiplier)))
                coords = ((32 - surf.get_width()) / 2, 32)
            else:
                coords = ((32 - surf.get_width()) / 2, 32 + self.animation_data['fraction'] * 32 * (self.Range * self.RangeMultiplier - 1))
        elif anim_direction == 'left':
            if self.animation_scale == ANIMATION_SCALE_SCALE:
                surf = pygame.transform.scale(surf, (int(32 * self.Range * self.RangeMultiplier), 32))
                coords = (-surf.get_width(), (32 - surf.get_height()) / 2)
            else:
                coords = (-surf.get_width() - self.animation_data['fraction'] * 32 * (self.Range * self.RangeMultiplier - 1), (32 - surf.get_height()) / 2)
        elif anim_direction == 'right':
            if self.animation_scale == ANIMATION_SCALE_SCALE:
                surf = pygame.transform.scale(surf, (int(32 * self.Range * self.RangeMultiplier), 32))
                coords = (32, (32 - surf.get_height()) / 2)
            else:
                coords = (32 + self.animation_data['fraction'] * 32 * (self.Range * self.RangeMultiplier - 1), (32 - surf.get_height()) / 2)
        elif anim_direction == 'circle':
            surf = pygame.transform.scale(surf, (32 + int(64 * self.Range * self.RangeMultiplier), 32 + int(64 * self.Range * self.RangeMultiplier)))
            coords = ((32 - surf.get_width()) / 2, (32 - surf.get_height()) / 2)
        elif anim_direction == 'line':
            enemy_coords = self.animation_data['attacked_enemy_coords']
            field = self.animation_data['enemy_field_relative']
            sprite = self.render()
            tower_source = (16, 32 - sprite.get_height() + 16)
            target_coords = (field[0] * 32 + enemy_coords[0] + 16, field[1] * 32 + enemy_coords[1] + 16)
            angle = math.atan2(target_coords[1] - tower_source[1], target_coords[0] - tower_source[0])
            deg = angle / math.pi * 180
            length = math.hypot(target_coords[0] - tower_source[0], target_coords[1] - tower_source[1])
            if self.animation_scale == ANIMATION_SCALE_SCALE:
                surf = pygame.transform.scale(surf, (int(length), surf.get_height()))
                surf = pygame.transform.rotate(surf, deg)
                coords = (min(target_coords[0], tower_source[0]), min(target_coords[1], tower_source[1]))
            else:
                w, h = surf.get_size()
                surf = pygame.transform.rotate(surf, -deg)
                surf_length = math.hypot(*surf.get_size())
                length_pos = self.animation_data['fraction'] * (length - surf_length)
                if length < surf_length:
                    length_pos =  length - surf_length - length_pos
                x = math.cos(angle) * length_pos
                y = math.sin(angle) * length_pos
                y_off = (surf.get_height() - math.sin(angle) * w) / 2
                x_off = (surf.get_width() - math.cos(angle) * w) / 2
                coords = (x - x_off + tower_source[0], y - y_off + tower_source[1])
            render_above = (target_coords[1] > 0)
        return surf, coords, render_above

    def Sell(self):
        self.WillSell=True

    def SetUpgradeCost(self, upgrade, cost):
        self.UpgradeCosts[upgrade]=cost

    def SetUpgradeMultiplier(self, upgrade, multiplier):
        self.UpgradeMultipliers[upgrade]=multiplier

    def Upgrade(self, upgrade):
        if self.UpgradeStatus[upgrade]!=UPGRADE_FALSE:
            raise IOError("This upgrade is already in use on this tower.")
        self.UpgradeStatus[upgrade]=UPGRADE_PENDING

    def setUpgradeSound(self, filename):
        self.UpgradeSound = filename

    def getValue(self):
        i=0
        value=self.Cost*self.SellPercentage/100
        for i in range(len(self.UpgradeStatus)):
            if self.UpgradeStatus[i] == UPGRADE_TRUE:
                value+=self.UpgradeCosts[i]*self.SellPercentageUpgrades/100
        return value

    def canUpgrades(self):
        upgrades=[False, False, False]
        if self.UpgradeStatus[UPGRADE_SPEED]==UPGRADE_FALSE and self.UpgradeCosts[UPGRADE_SPEED]>0:
            upgrades[UPGRADE_SPEED]=True
        if self.UpgradeStatus[UPGRADE_RANGE]==UPGRADE_FALSE and self.UpgradeCosts[UPGRADE_RANGE]>0:
            upgrades[UPGRADE_RANGE]=True
        if self.UpgradeStatus[UPGRADE_EFFECT]==UPGRADE_FALSE and self.UpgradeCosts[UPGRADE_EFFECT]>0:
            upgrades[UPGRADE_EFFECT]=True
        return upgrades

    def onUpgrade(self, upgrade):
        pass

    def setImpact(self, target, multiplier):
        self.Impacts[target]=multiplier

    def getImpact(self, target):
        if target in self.Impacts:
            return float(self.Impacts[target])
        return 1.0
