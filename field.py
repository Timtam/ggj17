import pygame
from random import randint

from commons import *
from constants import *

class Field:
    def __init__(self, screen, ftype, x, y, waytype, degree):
        self.x = x
        self.y = y
        self.screen = screen
        self.type  = ftype
        self.waytype = waytype
        self.degree = degree
        #0 - grass
        if self.type == FIELDTYPE_GRASS:
            self.sprite = get_common().get_image('assets/level/tiles/Maptiles_0.png')
        #1 - way
        elif self.type == FIELDTYPE_WAY:
            #0 - straight way
            if self.waytype == WAYTYPE_STRAIGHT:
                self.sprite = get_common().get_image('assets/level/tiles/Maptiles_2.png')
            elif self.waytype == WAYTYPE_CURVE:
                self.sprite = get_common().get_image('assets/level/tiles/Maptiles_1.png')

            self.sprite = self.rot_center(self.sprite, self.degree)
        #2 - decoration
        elif self.type == FIELDTYPE_DECORATION:
            if randint(1, 2) == 1:
                decoitem = 'wood'
                deconum = randint(1, 3)
            else:
                decoitem = 'rock'
                deconum = randint(1, 10)
            self.sprite = get_common().get_image('assets/level/decoration/' + decoitem + '_' + str(deconum) + '.png')
        #3 - flowers
        elif self.type == FIELDTYPE_FLOWERS:
            self.sprite = get_common().get_image('assets/level/decoration/' + 'Deko' + str(randint(1, 6)) + '.png')

        self.tower = None
        self.enemies = []

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def new_enemy(self, enemy):
        self.enemies.append(enemy())

    def set_tower(self, tower, every_way):
        self.tower = tower
        for i in range(16):
            if (self.x + i, self.y) in every_way:
                nearest_way = DIRECTION_RIGHT
                break;
            if (self.x - i, self.y) in every_way:
                nearest_way = DIRECTION_LEFT
                break;
            if (self.x, self.y + i) in every_way:
                nearest_way = DIRECTION_DOWN
                break;
            if (self.x, self.y - i) in every_way:
                nearest_way = DIRECTION_UP
                break;

        self.tower.set_direction(nearest_way)

    def get_type(self):
        return self.type

    def render_underground(self):
        return self.sprite
    def render_tower(self):
        return self.tower.render_tower()
    def render_tower_animation(self):
        return self.tower.render_animation()
    def render_deco(self):
        surf = pygame.Surface((32, 32), pygame.SRCALPHA)
        surf.blit(get_common().get_image('assets/level/tiles/Maptiles_0.png'), (0, 0))
        surf.blit(self.sprite, (0, 0))
        return surf


    def update_enemies(self, level):
        for enemy in self.enemies:
            enemy.update(level, self.x, self.y)
    def update_tower(self, level):
        if self.tower != None:
            self.tower.update(level, self.x, self.y)
