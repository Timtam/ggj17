from random import randint

from ..engine.enemy import Enemy

class Skeleton(Enemy):
    def __init__(self):
        super(Skeleton,self).__init__()
        self.health = self.max_health = 175
        self.speed = 1.25
        self.set_die_sound('assets/sound/skeleton/die.ogg')
        self.set_sprite('skeleton')
        self.drop = 9 + randint(-2, 2)
        self.name = 'skeleton'
