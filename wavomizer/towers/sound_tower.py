from ..engine.tower import Tower
from ..constants import *

class SoundTower(Tower):
    cost = 100
    effect_type = EFFECT_TYPE_DAMAGE | EFFECT_TYPE_CIRCLE | EFFECT_TYPE_ALL
    effect_value = 8.0
    attack_timeout = 1.0
    name = 'SOUND TOWER'
    description = 'As loud as Cannibal Corpse!'
    effect_desc = ('Deals ', '[damage]', ' AoE damage')

    def __init__(self, level):
        super(SoundTower, self).__init__(level)
        self.set_sprite('soundtower')
        self.set_place_sound("assets/sound/sound_tower/place.ogg")
        self.set_attack_sound("assets/sound/sound_tower/attack.ogg")
        self.set_upgrade_sound("assets/sound/sound_tower/upgrade.ogg")

        self.set_animation('assets/level/towers/sound')

        self.set_upgrade_cost(UPGRADE_SPEED, 70)
        self.set_upgrade_multiplier(UPGRADE_SPEED, 0.7)

        self.set_upgrade_cost(UPGRADE_EFFECT, 80)
        self.set_upgrade_multiplier(UPGRADE_EFFECT, 1.5)

        self.set_upgrade_cost(UPGRADE_RANGE, 100)
        self.set_upgrade_multiplier(UPGRADE_RANGE, 2.0)

    def on_upgrade(self, upgrade):
        if upgrade == UPGRADE_EFFECT:
            self.set_attack_sound('assets/sound/sound_tower/attack_upgrade.ogg')
            self.set_impact('golem', 0.75)
            self.set_impact('barrelguy', 0.8)
