from random import randint

from enemy import Enemy

class Golem(Enemy):
    def __init__(self):
        super(Golem,self).__init__()
        self.health = self.max_health = 1200
        self.speed = 1.75
        self.damage = 5
        self.set_die_sound('assets/sound/boss/die.ogg')
        self.set_arrival_sound('assets/sound/boss/arrival.ogg')
        self.set_hit_sound('assets/sound/boss/hit.ogg')
        self.set_sprite('golem')
        self.drop = 20 + randint(-5, 5)
        self.name = 'golem'
