from random import randint

from ..enemy import Enemy

class Barrel(Enemy):
    def __init__(self):
        super(Barrel,self).__init__()
        self.health = self.max_health = 100
        self.speed = 0.35
        self.set_die_sound('assets/sound/barrelguy/die.ogg')
        self.set_sprite('barrel')
        self.drop = 6 + randint(-2, 2)
        self.name = 'barrelguy'
