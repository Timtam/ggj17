import pygame
from random import randint

from ..commons import *
from ..constants import *

class Field:
    def __init__(self, level, ftype, x, y, waytype, degree):
        self.level = level
        self.x = x
        self.y = y
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
            self.sprite = get_common().get_image('assets/level/tiles/Maptiles_0.png').copy()
            self.sprite.blit(get_common().get_image('assets/level/decoration/' + decoitem + '_' + str(deconum) + '.png'), (0, 0))
        #3 - flowers
        elif self.type == FIELDTYPE_FLOWERS:
            self.sprite = get_common().get_image('assets/level/tiles/Maptiles_0.png').copy()
            self.sprite.blit(get_common().get_image('assets/level/decoration/' + 'Deko' + str(randint(1, 6)) + '.png'), (0, 0))

    def rot_center(self, image, angle):
        orig_rect = image.get_rect()
        rot_image = pygame.transform.rotate(image, angle)
        rot_rect = orig_rect.copy()
        rot_rect.center = rot_image.get_rect().center
        rot_image = rot_image.subsurface(rot_rect).copy()
        return rot_image

    def get_type(self):
        return self.type

    def draw(self):
        return self.sprite
