from ..engine.tower import Tower
from ..constants import *

class WaterTower(Tower):
    cost = 80
    effect_type = EFFECT_TYPE_SLOWDOWN | EFFECT_TYPE_STRAIGHT
    effect_value = 40
    attack_timeout = 2
    range = 16
    name = 'TSUNAMI TOWER'
    description = 'Sends out Haitis Nightmare!'
    effect_desc = ('Slows one enemy in a line for ', '[stun]', '%')

    def __init__(self, level):
        super(WaterTower, self).__init__(level)
        self.set_sprite('watertower')
        self.set_place_sound('assets/sound/water_tower/place.ogg')
        self.set_attack_sound('assets/sound/water_tower/attack.ogg')
        self.set_upgrade_sound('assets/sound/water_tower/upgrade.ogg')

        self.set_animation('assets/level/towers/wave', 2, 5)
        self.animation_repeat = 1
        self.animation_speed = 1
        self.animation_type = ANIMATION_TYPE_TRANSLATE

        self.set_impact('golem', 1.2)

        self.set_upgrade_cost(UPGRADE_SPEED, 120)
        self.set_upgrade_multiplier(UPGRADE_SPEED, 0.6)

        # if 0, upgrade is not possible
        self.set_upgrade_cost(UPGRADE_RANGE, 0)

        self.set_upgrade_cost(UPGRADE_EFFECT, 80)
        self.set_upgrade_multiplier(UPGRADE_EFFECT, 1.4)

    def on_upgrade(self, upgrade):
        if upgrade == UPGRADE_EFFECT:
            self.set_attack_sound('assets/sound/sound_tower/attack_upgrade.ogg')
