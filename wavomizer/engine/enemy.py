from __future__ import division
import pygame

from ..commons import *
from ..constants import *
from . import game_time

class Enemy(object):
    def __init__(self, level):
        self.level = level
        self.health = None
        self.speed = None
        self.die_sound = None
        self.speed_multiplier = 1.0
        self.arrival_sound = None
        self.hit_sound = 'assets/sound/common/hit.ogg'
        self.sprites = []
        self.drop = 0
        self.damage = 1 # damage done to player's castle
        self.direction = DIRECTION_RIGHT
        self.start = game_time.time()
        self.die = 0
        self.health_empty = get_common().get_image('assets/ui/health_empty.png')
        # render coords in pixels of the enemy
        self.coords = (0, 0)
        # coordinates in grid coordinates of the field this enemy is currently on
        self.tile = (0, 0)
        self.name = ''

    def init(self, tile_x, tile_y):
        self.tile = (tile_x, tile_y)
        if self.arrival_sound != None:
            play_sound_fx(self.arrival_sound)

    def set_sprite(self, filename):
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_up.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_down.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_left.png'))
        self.sprites.append(get_common().get_image('assets/level/enemies/' + filename + '_right.png'))

    def render(self, surface):
        sprite = self.sprites[self.direction]
        coords = (self.tile[0] * TILE_SIZE + self.coords[0], self.tile[1] * TILE_SIZE + self.coords[1] - 5)

        surface.blit(sprite, (coords[0], coords[1] + 5))
        surface.blit(self.health_empty, (coords[0] + (sprite.get_width() - self.health_empty.get_width()) / 2, coords[1]))
        health_fract = max(0, self.health / self.max_health)
        health_full = pygame.Surface((int(health_fract * 30), 2), pygame.SRCALPHA)
        if health_fract > 0.5:
            health_full.fill(pygame.Color(0, 170, 0, 255))
        elif health_fract > 0.25:
            health_full.fill(pygame.Color(200, 200, 0, 255))
        else:
            health_full.fill(pygame.Color(255, 0, 0, 255))
        surface.blit(health_full, (coords[0] + (sprite.get_width() - self.health_empty.get_width()) / 2 + 1, coords[1] + 1))
        return

    def set_die_sound(self, filename):
        self.die_sound = filename

    def set_arrival_sound(self, filename):
        self.arrival_sound = filename

    def set_hit_sound(self, filename):
        self.hit_sound = filename

    def get_drop(self):
        return self.drop

    def update(self, game_screen):
        if self.die > 0:
            # enemy is told to die, so do it now
            self.level.remove_enemy(self)
            game_screen.remove_enemy(self)
            if self.die == DIE_DAMAGE:
                play_sound_fx('assets/sound/common/coin.ogg')
            elif self.die == DIE_SUCCESS:
                play_sound_fx(self.hit_sound)
            return

        new_tile = False

        tile_fraction = (game_time.time() - self.start) / (self.speed * self.speed_multiplier)
        if tile_fraction >= 1:
            index = self.level.get_way().index(self.tile)
            if index == 0:
                self.die = DIE_SUCCESS
                return

            next = self.level.get_way()[index - 1]
            self.tile = next
            self.start = game_time.time()
            self.corner = False
            new_tile = True

        elif tile_fraction >= 0.5:
            index = self.level.get_way().index(self.tile)
            next = self.level.get_way()[index - 1]
            # x stays the same, y increases => down
            if self.tile[0] == next[0] and self.tile[1] < next[1]:
                self.direction = DIRECTION_DOWN
            # x stays the same, y decreases => up
            if self.tile[0] == next[0] and self.tile[1] > next[1]:
                self.direction = DIRECTION_UP
            # y stays the same, x decreases => left
            if self.tile[1] == next[1] and self.tile[0] < next[0]:
                self.direction = DIRECTION_RIGHT
            # y stays the same, x increases => right
            if self.tile[1] == next[1] and self.tile[0] > next[0]:
                self.direction = DIRECTION_LEFT

        # update render coords
        tile_fraction = (game_time.time() - self.start) / (self.speed * self.speed_multiplier)
        sprite_half_width = self.sprites[self.direction].get_width() / 2
        sprite_half_height = self.sprites[self.direction].get_height() / 2
        old_coords = self.coords
        if self.direction == DIRECTION_RIGHT:
            self.coords = (-sprite_half_width + tile_fraction * TILE_SIZE, 0)
            if old_coords[0] > self.coords[0] and new_tile:
                self.coord = old_coords
        elif self.direction == DIRECTION_LEFT:
            self.coords = (sprite_half_width - tile_fraction * TILE_SIZE, 0)
            if old_coords[0] < self.coords[0] and new_tile:
                self.coord = old_coords
        elif self.direction == DIRECTION_UP:
            self.coords = (0, sprite_half_height - tile_fraction * TILE_SIZE)
            if old_coords[1] > self.coords[1] and new_tile:
                self.coord = old_coords
        elif self.direction == DIRECTION_DOWN:
            self.coords = (0, -sprite_half_height + tile_fraction * TILE_SIZE)
            if old_coords[1] < self.coords[1] and new_tile:
                self.coord = old_coords

    def add_health(self, health):
        self.health += health
        if self.health <= 0:
            self.die = DIE_DAMAGE
            play_sound_fx(self.die_sound)
