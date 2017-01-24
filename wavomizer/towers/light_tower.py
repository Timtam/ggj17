from ..engine.tower import Tower
from ..constants import *

class LightTower(Tower):
    cost = 90
    name = 'LIGHTWAVE TOWER'
    description = 'Lumos Maxima! Deals damage to single targets with high\n concentrated power of will.'
    effect_desc = ('Deals damage to the target enemy by ', '[slow]', 'dps')

    def __init__(self):
        super(LightTower, self).__init__()
        self.effect_type = EFFECT_TYPE_DAMAGE
        self.effect_value = 10.5 # damage
        self.attack_timeout = 0.5 # in seconds
        self.set_sprite('lighttower')
        self.set_place_sound('assets/sound/light_tower/place.ogg')
        self.set_attack_sound('assets/sound/light_tower/attack.ogg')
        self.set_upgrade_sound('assets/sound/light_tower/upgrade.ogg')

        self.set_animation('assets/level/towers/light')
        self.animation_speed = 4
        self.animation_type = ANIMATION_TYPE_TRANSLATE

        self.set_impact('ghost', 0.9)

        self.set_upgrade_cost(UPGRADE_SPEED, 55)
        self.set_upgrade_multiplier(UPGRADE_SPEED, 0.8)

        self.set_upgrade_cost(UPGRADE_RANGE, 65)
        self.set_upgrade_multiplier(UPGRADE_RANGE, 2.0)

        self.set_upgrade_cost(UPGRADE_EFFECT, 75)
        self.set_upgrade_multiplier(UPGRADE_EFFECT, 1.5)

    def on_upgrade(self, upgrade):
        if upgrade == UPGRADE_EFFECT:
            self.set_attack_sound('assets/sound/sound_tower/attack_upgrade.ogg')
            self.set_impact('barrelguy', 1.1)
