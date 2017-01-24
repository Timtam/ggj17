from __future__ import division
import pygame
import time

from ..commons import *
from ..constants import *

class Enemy(object):
    def __init__(self):
        self.health = None
        self.speed = None
        self.die_sound = None
        self.speed_multiplier = 1.0
        self.arrival_sound = None
        self.hit_sound = "assets/sound/common/hit.ogg"
        self.sprites = []
        self.drop = 0
        self.damage = 1 # damage done to player's castle
        self.direction = DIRECTION_RIGHT
        self.start = time.time()
        self.die = 0
        self.health_empty = get_common().get_image('assets/ui/health_empty.png')
        # render coords in pixels of the enemy relative to its current field
        self.coords = (0, 0)
        # coordinates in grid coordinates of the field this enemy is currently on
        self.field = (0, 0)
        self.name = ''

    def init(self):
        if self.arrival_sound != None:
            play_sound_fx(self.arrival_sound)

    def set_sprite(self, filename):
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_up.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_down.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_left.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_right.png'))

    def render(self):
        sprite = self.sprites[self.direction]
        coords = (self.coords[0], self.coords[1] - 5)
        surf = pygame.Surface((sprite.get_width(), sprite.get_height() + 5), pygame.SRCALPHA)
        surf.blit(sprite, (0, 5))

        surf.blit(self.health_empty, (sprite.get_width() / 2 - 16, 0))
        health_fract = max(0, self.health / self.max_health)
        health_full = pygame.Surface((int(health_fract * 30), 2), pygame.SRCALPHA)
        if health_fract > 0.5:
            health_full.fill(pygame.Color(0, 170, 0, 255))
        elif health_fract > 0.25:
            health_full.fill(pygame.Color(200, 200, 0, 255))
        else:
            health_full.fill(pygame.Color(255, 0, 0, 255))
        surf.blit(health_full, (sprite.get_width() / 2 - 15, 1))
        return surf, coords

    def set_die_sound(self, filename):
        self.die_sound = filename

    def set_arrival_sound(self, filename):
        self.arrival_sound = filename

    def set_hit_sound(self, filename):
        self.hit_sound = filename

    def get_drop(self):
        return self.drop

    def update(self, level, x, y):
        if self.die > 0:
            # enemy is told to die, so do it now
            del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])
            level.remove_enemy(self)
            if self.die == DIE_DAMAGE:
                play_sound_fx('assets/sound/common/coin.ogg')
            elif self.die == DIE_SUCCESS:
                play_sound_fx(self.hit_sound)
            return
        self.field = (x, y)

        new_field = False

        if (time.time() - self.start) > (self.speed * self.speed_multiplier):
            index = level.way.index((x, y))
            if index == 0:
                self.die = DIE_SUCCESS
                return

            next = level.way[index - 1]
            # x stays the same, y increases => down
            if x == next[0] and y < next[1]:
                self.direction = DIRECTION_DOWN
            # x stays the same, y decreases => up
            if x == next[0] and y > next[1]:
                self.direction = DIRECTION_UP
            # y stays the same, x decreases => left
            if y == next[1] and x < next[0]:
                self.direction = DIRECTION_RIGHT
            # y stays the same, x increases => right
            if y == next[1] and x > next[0]:
                self.direction = DIRECTION_LEFT

            self.field = (next[0], next[1])
            field = level.grid[next[0]][next[1]]
            self.start = time.time()
            self.corner = False
            field.enemies.append(self)
            new_field = True
            del(level.grid[x][y].enemies[level.grid[x][y].enemies.index(self)])

        # update render coords
        sprite_half_width = self.sprites[self.direction].get_width() / 2
        sprite_half_height = self.sprites[self.direction].get_height() / 2
        old_coords = self.coords
        if self.direction == DIRECTION_RIGHT:
            self.coords = ((-1) * sprite_half_width + ((time.time() - self.start) * 32 / (self.speed * self.speed_multiplier)) - 16 , 0)
            if old_coords[0] > self.coords[0] and new_field:
                self.coord = old_coords
        elif self.direction == DIRECTION_LEFT:
            self.coords = (sprite_half_width - ((time.time() - self.start) * 32 / (self.speed * self.speed_multiplier)) + 16, 0)
            if old_coords[0] < self.coords[0] and new_field:
                self.coord = old_coords
        elif self.direction == DIRECTION_UP:
            self.coords = (0, sprite_half_height - ((time.time() - self.start) * 32 / (self.speed * self.speed_multiplier)) + 16)
            if old_coords[1] > self.coords[1] and new_field:
                self.coord = old_coords
        elif self.direction == DIRECTION_DOWN:
            self.coords = (0, (-1) * sprite_half_height + ((time.time() - self.start) * 32 / (self.speed * self.speed_multiplier)) - 16)
            if old_coords[0] < self.coords[0] and new_field:
                self.coord = old_coords

    def add_health(self, health):
        self.health += health
        if self.health <= 0:
            self.die = DIE_DAMAGE
            play_sound_fx(self.die_sound)
