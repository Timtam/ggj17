from random import randint

from wavomizer.enemy import Enemy

class Ghost(Enemy):
    def __init__(self):
        super(Ghost, self).__init__()
        self.health = self.max_health = 150
        self.speed = 0.75
        self.set_die_sound('assets/sound/ghost/die.ogg')
        self.set_sprite('ghost')
        self.drop = 7 + randint(-2, 2)
        self.name = 'ghost'
