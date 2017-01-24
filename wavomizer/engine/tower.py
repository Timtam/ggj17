from random import randint
import pygame
import math
import time
import os, os.path

from ..commons import *
from ..constants import *
import field

class Tower(object):
    cost=0

    def __init__(self):
        self.effect_type = EFFECT_TYPE_NONE
        self.effect_multiplier = 1.0
        self.effect_value = 0
        self.attack_timeout = 10.0 # in seconds
        self.attack_timeout_multiplier = 1.0
        self.range = 1 # one tile radius
        self.range_multiplier = 1.0
        self.sprites = []
        self.place_sound = None
        self.attack_sound = None
        self.pending_transaction = 0
        self.last_fire = 0
        self.enemy_cache = [] # saves all enemies which shouldn't be attacked again
        self.will_sell = False
        self.sell_percentage = 50
        self.sell_percentage_upgrades = 30
        self.upgrade_costs = [0, 0, 0]
        self.upgrade_multipliers = [0.0, 0.0, 0.0]
        self.upgrade_status = [UPGRADE_FALSE, UPGRADE_FALSE, UPGRADE_FALSE]
        self.upgrade_sound = None
        self.impacts = {}
        self.direction = DIRECTION_UP
        self.animations = {}
        self.animation_fraction = 0
        self.animation_playing = False
        self.animation_direction = ANIMATION_DIRECTION_SELF
        self.animation_target_enemy = None
        self.animation_target_enemy_field_coords = (0, 0)
        self.animation_target_enemy_relative_pixels = (0, 0)
        self.animation_repeat = 1
        self.animation_speed = 1
        self.animation_type = ANIMATION_TYPE_SCALE

    def init(self, pay = True):
        if pay:
            # setting pending_transaction to the costs of the tower on first run, so the player needs to pay
            self.pending_transaction = self.cost
            play_sound_fx(self.place_sound)

        # set animation direction
        if self.effect_type & EFFECT_TYPE_CIRCLE == EFFECT_TYPE_CIRCLE:
            # circle effect uses circle animation
            self.animation_direction = ANIMATION_DIRECTION_CIRCLE
        elif self.effect_type & EFFECT_TYPE_STRAIGHT == EFFECT_TYPE_STRAIGHT:
            # straight effect uses tower's direction for animation
            self.animation_direction = ANIMATION_DIRECTION_SELF
        else:
            # targeted effect uses straight line for animation
            self.animation_direction = ANIMATION_DIRECTION_LINE

    # finds all valid target fields
    def find_target_fields(self, fields, x, y):
        # range to search for valid target fields
        # clamped to the size of the 2d fields array
        min_x = max(0, x - int(self.range * self.range_multiplier))
        max_x = min(len(fields) - 1, x + int(self.range * self.range_multiplier))
        min_y = max(0, y - int(self.range * self.range_multiplier))
        max_y = min(len(fields[0]) - 1, y + int(self.range * self.range_multiplier))

        valid_targets = [] # contains x and y tuples
        if math.floor(self.range * self.range_multiplier) != self.range * self.range_multiplier:
            raise IOError('range * range_multiplier = {0}, but only integers are allowed'.format(str(self.range * self.range_multiplier)))
        for field_x in range(min_x, max_x + 1):
            for field_y in range(min_y, max_y + 1):
                if field_x == x and field_y == y:
                    continue
                if self.effect_type & EFFECT_TYPE_STRAIGHT == EFFECT_TYPE_STRAIGHT and (
                    (self.direction == DIRECTION_UP and (field_x != x or field_y >= y)) or
                    (self.direction == DIRECTION_RIGHT and (field_x <= x or field_y != y)) or
                    (self.direction == DIRECTION_DOWN and (field_x != x or field_y <= y)) or
                    (self.direction == DIRECTION_LEFT and (field_x >= x or field_y != y))):
                    continue
                valid_targets.append((field_x, field_y))
        return valid_targets

    # needs all valid target fields as tuple array, as returned by find_target_fields
    # returns all actual targets (deal damage here) as tuple-array
    def filter_target_fields(self, level, valid_targets):
        enemies = []
        nearest_field = None
        targets = []
        # filter all fields without enemies
        for i in range(len(valid_targets)):
            enemies = []
            target_field = level.grid[valid_targets[i][0]][valid_targets[i][1]]
            if target_field.get_type() != field.FIELDTYPE_WAY:
                continue
            for j in range(len(target_field.enemies)):
                enemy = target_field.enemies[j]
                if self.effect_type & EFFECT_TYPE_SLOWDOWN == EFFECT_TYPE_SLOWDOWN and enemy in self.enemy_cache:
                    continue
                enemies.append(enemy)
            if len(enemies) == 0:
                continue
            targets.append(valid_targets[i])
        # no targets left?
        if len(targets) == 0:
            return []
        if self.effect_type & EFFECT_TYPE_CIRCLE != EFFECT_TYPE_CIRCLE:
            # filtering down to just one valid field, only one field should be attacked
            # per definition (Henry) this should be the field with the lowest distance to the target
            nearest_field = targets[0]
            for i in range(1, len(targets)):
                if level.way.index((targets[i][0], targets[i][1])) < level.way.index((nearest_field[0], nearest_field[1])):
                    nearest_field = targets[i]
            targets = [nearest_field]
        return targets

    def set_direction(self, nearestWay):
        self.direction = nearestWay

    def update_transactions(self, level, x, y):
        if self.will_sell == True:
            level.grid[x][y].tower = None
            level.cash += self.get_value()
            self.will_sell = False
            play_sound_fx('assets/sound/common/sell.ogg')
            play_sound_fx('assets/sound/common/coin.ogg')
            return True
        for i in range(len(self.upgrade_status)):
            if self.upgrade_status[i] == UPGRADE_PENDING:
                self.pending_transaction += self.upgrade_costs[i]
                self.upgrade_status[i] = UPGRADE_TRUE
                if i == UPGRADE_SPEED:
                    self.attack_timeout_multiplier = self.upgrade_multipliers[i]
                elif i == UPGRADE_RANGE:
                    self.range_multiplier = self.upgrade_multipliers[i]
                elif i == UPGRADE_EFFECT:
                    self.effect_multiplier = self.upgrade_multipliers[i]
                if self.upgrade_sound != None:
                    play_sound_fx(self.upgrade_sound)
                self.on_upgrade(i)
        # pay the crystals required for buying or upgrading this tower
        if self.pending_transaction > 0:
            if self.pending_transaction > level.cash:
                raise IOError('User wants to build or upgrade tower, but doesn\'t have enough money. Please try again later!')
            level.cash -= self.pending_transaction
            self.pending_transaction = 0

    def update_animation(self, level, x, y):
        if self.animation_playing:
            anim_fraction = (time.time() - self.last_fire) / (self.attack_timeout_multiplier * self.attack_timeout) * self.animation_speed
            if anim_fraction >= 1:
                self.animation_playing = False
                self.animation_fraction = 0
            else:
                self.animation_fraction = (anim_fraction * self.animation_repeat) %  1
            if self.animation_target_enemy != None:
                self.animation_target_enemy_pixel_coords = self.animation_target_enemy.coords
                self.animation_target_enemy_field_relative = (self.animation_target_enemy.field[0] - x, self.animation_target_enemy.field[1] - y)

    def update_attack(self, level, x, y):
        if (time.time() - self.last_fire) < (self.attack_timeout_multiplier * self.attack_timeout):
            return
        valid_targets = self.find_target_fields(level.grid, x, y)
        valid_targets = self.filter_target_fields(level, valid_targets)
        if len(valid_targets)==0:
            return
        for i in range(len(valid_targets)):
            target_field = level.grid[valid_targets[i][0]][valid_targets[i][1]]
            if self.effect_type & EFFECT_TYPE_ALL == EFFECT_TYPE_ALL:
                for j in range(len(target_field.enemies)):
                    enemy = target_field.enemies[j]
                    if self.effect_type & EFFECT_TYPE_DAMAGE == EFFECT_TYPE_DAMAGE:
                        enemy.add_health(-self.get_impact(enemy.name) * self.effect_multiplier * self.effect_value)
                    elif self.effect_type & EFFECT_TYPE_SLOWDOWN == EFFECT_TYPE_SLOWDOWN:
                        if enemy in self.enemy_cache:
                            continue
                        enemy.speed_multiplier += self.get_impact(enemy.name) * self.effect_multiplier * self.effect_value * enemy.speed_multiplier / 100.0
                        self.enemy_cache.append(enemy)
            else:
                enemies = []
                for j in range(len(target_field.enemies)):
                    if self.effect_type & EFFECT_TYPE_SLOWDOWN == EFFECT_TYPE_SLOWDOWN and target_field.enemies[j] in self.enemy_cache:
                        continue
                    enemies.append(target_field.enemies[j])
                if len(enemies) == 0:
                    return
                enemy = enemies[randint(0, len(enemies) - 1)]
                self.animation_target_enemy = enemy
                if self.effect_type & EFFECT_TYPE_DAMAGE == EFFECT_TYPE_DAMAGE:
                    enemy.add_health(-self.get_impact(enemy.name) * self.effect_multiplier * self.effect_value)
                elif self.effect_type & EFFECT_TYPE_SLOWDOWN == EFFECT_TYPE_SLOWDOWN:
                    enemy.speed_multiplier += self.get_impact(enemy.name) * self.effect_multiplier * self.effect_value * enemy.speed_multiplier / 100.0
                    self.enemy_cache.append(enemy)
            if self.attack_sound != None:
                play_sound_fx(self.attack_sound)
            self.last_fire = time.time()
            self.animation_playing = True

    def update(self, level, x, y):
        if self.update_transactions(level, x, y): return
        if self.update_attack(level, x, y): return
        if self.update_animation(level, x, y): return

    def set_sprite(self, path):
        self.sprites.append(get_common().get_image('assets/level/towers/' + path + '_up.png'))
        self.sprites.append(get_common().get_image('assets/level/towers/' + path + '_down.png'))
        self.sprites.append(get_common().get_image('assets/level/towers/' + path + '_left.png'))
        self.sprites.append(get_common().get_image('assets/level/towers/' + path + '_right.png'))

    def set_place_sound(self, filename):
        self.place_sound = filename

    def set_attack_sound(self, filename):
        self.attack_sound = filename

    def set_animation(self, path, repeat_frames = 0, repeat_count = 0):
        animation_name = path[(path.rfind('/') + 1):] + '_'
        animation_directions = {ANIMATION_DIRECTION_UP: 'up', ANIMATION_DIRECTION_DOWN: 'down', ANIMATION_DIRECTION_LEFT: 'left', ANIMATION_DIRECTION_RIGHT: 'right', ANIMATION_DIRECTION_CIRCLE: 'circle', ANIMATION_DIRECTION_LINE: 'line'}
        for direction in animation_directions.keys():
            text_direction = animation_directions[direction]
            dir_path = path + '_' + text_direction + '/'
            base_file_name = animation_name + text_direction + '_'
            if os.path.exists(dir_path):
                self.animations[direction] = []
                files = [f for f in os.listdir(dir_path) if os.path.isfile(dir_path + f) and f.startswith(base_file_name)]
                files.sort()
                for f in files:
                    self.animations[direction].append(get_common().get_image(dir_path + f))
                for i in range(repeat_count * repeat_frames):
                    self.animations[direction].append(self.animations[direction][-repeat_frames])

    def get_sprite(self):
        return self.sprites[self.direction]

    def render_tower(self):
        sprite = self.get_sprite()
        surf = pygame.Surface(sprite.get_size(), pygame.SRCALPHA)
        surf.blit(sprite, (0, 0))

        if self.upgrade_status[UPGRADE_EFFECT] == UPGRADE_TRUE:
            surf.blit(get_common().get_image('assets/level/towers/upgrade_effect.png'), (2, 10))
        if self.upgrade_status[UPGRADE_RANGE] == UPGRADE_TRUE:
            surf.blit(get_common().get_image('assets/level/towers/upgrade_range.png'), (2, 20))
        if self.upgrade_status[UPGRADE_SPEED] == UPGRADE_TRUE:
            surf.blit(get_common().get_image('assets/level/towers/upgrade_speed.png'), (2, 30))

        return surf

    def render_animation(self):
        anim_direction = self.animation_direction
        if anim_direction == ANIMATION_DIRECTION_SELF:
            anim_direction = self.direction
        if anim_direction not in self.animations or not self.animation_playing:
            return pygame.Surface((0, 0), pygame.SRCALPHA), (0, 0), False

        animation = self.animations[anim_direction]
        animation_index = int(math.floor(len(animation) * self.animation_fraction))
        surf = animation[animation_index]
        render_above = False

        field_size = 32

        # calculate animation coords and render animation
        # animation coords are relative to the top left corner of the field the tower is on
        if anim_direction == ANIMATION_DIRECTION_UP:
            y = 0 # y coord of animation's bottom
            if self.animation_type == ANIMATION_TYPE_SCALE:
                # scale animation to full range
                surf = pygame.transform.scale(surf, (surf.get_width(), int(field_size * self.range * self.range_multiplier)))
            else:
                # move animation to correct position
                total_length = field_size * self.range * self.range_multiplier - surf.get_height()
                y = - self.animation_fraction * total_length
            coords = ((field_size - surf.get_width()) / 2, y - surf.get_height())

        elif anim_direction == ANIMATION_DIRECTION_DOWN:
            y = 0 # y coord of animation's top
            if self.animation_type == ANIMATION_TYPE_SCALE:
                # scale animation to full range
                surf = pygame.transform.scale(surf, (surf.get_width(), int(field_size * self.range * self.range_multiplier)))
            else:
                # move animation to correct position
                total_length = field_size * self.range * self.range_multiplier - surf.get_height()
                y = self.animation_fraction * total_length
            coords = ((field_size - surf.get_width()) / 2, y + field_size)

        elif anim_direction == ANIMATION_DIRECTION_LEFT:
            x = 0
            if self.animation_type == ANIMATION_TYPE_SCALE:
                surf = pygame.transform.scale(surf, (int(field_size * self.range * self.range_multiplier), surf.get_height()))
            elif self.animation_type == ANIMATION_TYPE_TRANSLATE:
                total_length = field_size * self.range * self.range_multiplier - surf.get_width()
                x = - self.animation_fraction * total_length
            coords = (x - surf.get_width(), (field_size - surf.get_height()) / 2)

        elif anim_direction == ANIMATION_DIRECTION_RIGHT:
            x = 0
            if self.animation_type == ANIMATION_TYPE_SCALE:
                surf = pygame.transform.scale(surf, (int(field_size * self.range * self.range_multiplier), surf.get_height()))
            elif self.animation_type == ANIMATION_TYPE_TRANSLATE:
                total_length = field_size * self.range * self.range_multiplier - surf.get_width()
                x = self.animation_fraction * total_length
            coords = (x + field_size, (field_size - surf.get_height()) / 2)

        elif anim_direction == ANIMATION_DIRECTION_CIRCLE:
            # scale animation to full range of the tower, translating doesn't make sense here
            size = field_size + int(field_size * 2 * self.range * self.range_multiplier)
            surf = pygame.transform.scale(surf, (size, size))
            coords = ((field_size - surf.get_width()) / 2, (field_size - surf.get_height()) / 2)

        elif anim_direction == ANIMATION_DIRECTION_LINE:
            enemy_coords = self.animation_target_enemy_pixel_coords
            field = self.animation_target_enemy_field_relative
            sprite = self.get_sprite()
            # coords where the line starts (still relative to top left corner of field)
            tower_source = (field_size / 2, field_size - sprite.get_height() + 16)
            # coords where the line ends
            target_coords = (field[0] * field_size + enemy_coords[0] + field_size / 2, field[1] * field_size + enemy_coords[1] + field_size / 2)
            # angle of the line
            angle = math.atan2(target_coords[1] - tower_source[1], target_coords[0] - tower_source[0])
            deg = angle / math.pi * 180
            # length of the line
            length = math.hypot(target_coords[0] - tower_source[0], target_coords[1] - tower_source[1])
            if self.animation_type == ANIMATION_TYPE_SCALE:
                # scale animation to correct length
                surf = pygame.transform.scale(surf, (int(length), surf.get_height()))
                # rotate animation
                surf = pygame.transform.rotate(surf, -deg)
                coords = (min(target_coords[0], tower_source[0]), min(target_coords[1], tower_source[1]))
            elif self.animation_type == ANIMATION_TYPE_TRANSLATE:
                w, h = surf.get_size()
                # rotate animation
                surf = pygame.transform.rotate(surf, -deg)
                # get length of rotated animation
                surf_length = math.hypot(*surf.get_size())
                # position of the animation along the line
                length_pos = self.animation_fraction * (length - surf_length)
                # move animation back when the length to move is negative
                if length < surf_length:
                    length_pos =  length - surf_length - length_pos
                # coords of animation on the line relative to start of the line
                x = math.cos(angle) * length_pos
                y = math.sin(angle) * length_pos
                # coords of the middle of the left side of the animation after the rotation
                # these coords allow animation with a significant height to be aligned correctly
                y_off = (surf.get_height() - math.sin(angle) * w) / 2
                x_off = (surf.get_width() - math.cos(angle) * w) / 2
                # calculate final render coords
                coords = (x - x_off + tower_source[0], y - y_off + tower_source[1])
            render_above = (target_coords[1] > 0)
        return surf, coords, render_above

    def sell(self):
        self.will_sell=True

    def set_upgrade_cost(self, upgrade, cost):
        self.upgrade_costs[upgrade] = cost

    def set_upgrade_multiplier(self, upgrade, multiplier):
        self.upgrade_multipliers[upgrade] = multiplier

    def upgrade(self, upgrade):
        if self.upgrade_status[upgrade] != UPGRADE_FALSE:
            raise IOError("This upgrade is already in use on this tower.")
        self.upgrade_status[upgrade] = UPGRADE_PENDING

    def set_upgrade_sound(self, filename):
        self.upgrade_sound = filename

    def get_value(self):
        value = self.cost * self.sell_percentage / 100
        for i in range(len(self.upgrade_status)):
            if self.upgrade_status[i] == UPGRADE_TRUE:
                value += self.upgrade_costs[i] * self.sell_percentage_upgrades / 100
        return int(value)

    def can_upgrades(self):
        upgrades = [False, False, False]
        if self.upgrade_status[UPGRADE_SPEED] == UPGRADE_FALSE and self.upgrade_costs[UPGRADE_SPEED] > 0:
            upgrades[UPGRADE_SPEED] = True
        if self.upgrade_status[UPGRADE_RANGE] == UPGRADE_FALSE and self.upgrade_costs[UPGRADE_RANGE] > 0:
            upgrades[UPGRADE_RANGE] = True
        if self.upgrade_status[UPGRADE_EFFECT] == UPGRADE_FALSE and self.upgrade_costs[UPGRADE_EFFECT] > 0:
            upgrades[UPGRADE_EFFECT] = True
        return upgrades

    def on_upgrade(self, upgrade):
        pass

    def set_impact(self, target, multiplier):
        self.impacts[target] = multiplier

    def get_impact(self, target):
        if target in self.impacts:
            return float(self.impacts[target])
        return 1.0
