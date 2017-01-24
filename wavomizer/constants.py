# effect types can be combined (e.g. to deal damage and stop enemies)
EFFECT_TYPE_NONE = 0x00 # no effect at all
EFFECT_TYPE_DAMAGE = 0x01 # tower will deal damage to one single opponent, EffectValue equals real damage
EFFECT_TYPE_SLOWDOWN = 0x02 # slow down opponents, EffectValue equals percentage of slowdown (compared to enemy speed)
EFFECT_TYPE_ALL = 0x04 # all targets on best field
EFFECT_TYPE_CIRCLE = 0x08 # all enemies in range
EFFECT_TYPE_STRAIGHT = 0x10 # target only straight forward (obviously not together with circle^^)

ANIMATION_TYPE_SCALE = 0 # scale animation to correct size
ANIMATION_TYPE_TRANSLATE = 1 # move animation from start to end instead of scaling

ANIMATION_DIRECTION_UP = 0 # animation will play upwards from the tower
ANIMATION_DIRECTION_DOWN = 1 # animation will play downwards from the tower
ANIMATION_DIRECTION_LEFT = 2 # animation will play to the left of the tower
ANIMATION_DIRECTION_RIGHT = 3 # animation will play to the rightt of the tower
ANIMATION_DIRECTION_SELF = 4 # animation will play in the direction the tower is pointing
ANIMATION_DIRECTION_LINE = 5 # animation will play in a straight line to the current target
ANIMATION_DIRECTION_CIRCLE = 6 # animation will play in a circle around the tower

UPGRADE_SPEED = 0
UPGRADE_EFFECT = 1
UPGRADE_RANGE=2

UPGRADE_FALSE = 0
UPGRADE_PENDING = 1
UPGRADE_TRUE = 2

DIRECTION_UP = 0
DIRECTION_DOWN = 1
DIRECTION_LEFT = 2
DIRECTION_RIGHT = 3

DIE_DAMAGE=1
DIE_SUCCESS=2

FIELDTYPE_GRASS = 0
FIELDTYPE_WAY = 1
FIELDTYPE_DECORATION = 2
FIELDTYPE_FLOWERS = 3

WAYTYPE_STRAIGHT = 0
WAYTYPE_CURVE = 1

# size of a single tile of the level in pixels
TILE_SIZE = 32
# size of the level grid in tiles
GRID_SIZE = 16
# size of the level grid in pixels
GRID_PIXEL_SIZE = GRID_SIZE * TILE_SIZE
