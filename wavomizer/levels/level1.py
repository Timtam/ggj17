from ..engine.level import Level
from ..enemies.ghost import Ghost
from ..enemies.skeleton import Skeleton
from ..enemies.barrel import Barrel
from ..enemies.golem import Golem

class Level1(Level):
    way = [
        ( 1, 12), ( 2, 12), ( 3, 12), ( 3, 11), ( 3, 10), ( 4, 10), ( 5, 10), ( 6, 10), ( 6,  9), ( 6,  8), ( 6,  7), ( 5,  7), ( 4,  7),
        ( 4,  6), ( 3,  6), ( 3,  5), ( 3,  4), ( 3,  3), ( 4,  3), ( 5,  3), ( 6,  3), ( 7,  3), ( 8,  3), ( 8,  4), ( 8,  5), ( 9,  5),
        ( 9,  6), ( 9,  7), ( 9,  8), ( 9,  9), ( 9, 10), ( 9, 11), ( 9, 12), ( 9, 13), (10, 13), (11, 13), (12, 13), (13, 13), (13, 12),
        (13, 11), (13, 10), (13,  9), (13,  8), (12,  8), (12,  7), (12,  6), (13,  6), (13,  5)]
    possible_flowers = [
        ( 0,  0), ( 1,  0), ( 2,  0), ( 3,  0), ( 4,  0), ( 5,  0), ( 6,  0), ( 7,  0), ( 8,  0), ( 9,  0), (10,  0), (11,  0), (12,  0),
        (13,  0), (14,  0), (15,  0), ( 0,  1), ( 1,  1), ( 2,  1), ( 3,  1), ( 4,  1), ( 5,  1), ( 6,  1), ( 7,  1), ( 8,  1), ( 9,  1),
        (10,  1), (11,  1), (12,  1), (15,  1), ( 0,  2), ( 1,  2), ( 2,  2), ( 3,  2), ( 4,  2), ( 5,  2), ( 6,  2), ( 7,  2), ( 8,  2),
        ( 9,  2), (10,  2), (11,  2), (12,  2), ( 0,  3), ( 1,  3), ( 2,  3), ( 9,  3), (10,  3), ( 0,  4), ( 1,  4), ( 2,  4), ( 4,  4),
        ( 5,  4), ( 6,  4), ( 7,  4), ( 9,  4), (10,  4), ( 0,  5), ( 1,  5), ( 2,  5), ( 4,  5), ( 5,  5), ( 6,  5), ( 7,  5), (10,  5),
        (11,  5), ( 0,  6), ( 1,  6), ( 2,  6), ( 5,  6), ( 6,  6), ( 7,  6), ( 8,  6), (10,  6), (11,  6), (14,  6), (15,  6), ( 0,  7),
        ( 1,  7), ( 2,  7), ( 3,  7), ( 7,  7), ( 8,  7), (10,  7), (11,  7), (13,  7), (14,  7), (15,  7), ( 1,  8), ( 2,  8), ( 3,  8),
        ( 4,  8), ( 5,  8), ( 7,  8), ( 8,  8), (10,  8), (11,  8), (14,  8), (15,  8), ( 1,  9), ( 2,  9), ( 3,  9), ( 4,  9), ( 5,  9),
        ( 7,  9), ( 8,  9), (10,  9), (11,  9), (12,  9), (14,  9), (15,  9), ( 2, 10), ( 7, 10), ( 8, 10), (10, 10), (11, 10), (12, 10),
        (14, 10), (15, 10), ( 2, 11), ( 4, 11), ( 5, 11), ( 6, 11), ( 7, 11), ( 8, 11), (10, 11), (11, 11), (12, 11), (14, 11), (15, 11),
        ( 4, 12), ( 5, 12), ( 6, 12), ( 7, 12), ( 8, 12), (10, 12), (11, 12), (12, 12), (14, 12), (15, 12), ( 2, 13), ( 3, 13), ( 4, 13),
        ( 5, 13), ( 6, 13), ( 7, 13), ( 8, 13), (14, 13), (15, 13), ( 2, 14), ( 3, 14), ( 4, 14), ( 5, 14), ( 6, 14), ( 7, 14), ( 8, 14),
        ( 9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14), ( 2, 15), ( 3, 15), ( 4, 15), ( 5, 15), ( 6, 15), ( 7, 15),
        ( 8, 15), ( 9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)]
    possible_decoration = [
        ( 1,  1), ( 2,  1), ( 3,  1), ( 4,  1), ( 5,  1), ( 6,  1), ( 7,  1), ( 8,  1), ( 9,  1), (10,  1), ( 1,  2), (10,  2), (11, 10),
        (11, 11), ( 1,  3), ( 1,  4), ( 1,  5), ( 1,  6), ( 1,  7), ( 1,  8), ( 2,  8), ( 6,  5), ( 6, 12), ( 5, 13), ( 6, 13), ( 3, 14),
        ( 4, 14), ( 5, 14), ( 6, 14), ( 7, 14)]
    waves = [
        ('level1.ogg', (
            (12, Skeleton, 3),)),
        ('level2.ogg', (
            (3, Skeleton, 2, 2),
            (3, Ghost, 4, 2),
            (3, Skeleton, 2, 1),
            (3, Skeleton, 2))),
        ('level3.ogg', (
            (8, Skeleton, 2, 2),
            (1, Barrel, 2),
            (2, Ghost, 2, 2))),
        ('level4.ogg', (
            (13, Skeleton, 2, 0.5),
            (5, Barrel, 2),
            (7, Ghost, 1, 3),
            (3, Barrel, 1))),
        ('level5.ogg', (
            (10, Skeleton, 1, 1),
            (10, Ghost, 1, 2),
            (11, Barrel, 1, 0.5),
            (1, Golem, 1, 0.2),
            (13, Ghost, 1))),
        ('level6.ogg', (
            (2, Golem, 0.5, 15),
            (10, Skeleton, 0.2, 0.4),
            (3, Ghost, 1, 1),
            (3, Barrel, 1, 1),
            (3, Skeleton, 1, 1),
            (3, Barrel, 1, 1),
            (3, Skeleton, 2, 1),
            (3, Skeleton, 0.4, 0.4),
            (3, Barrel, 1, 0.4),
            (3, Skeleton, 0.4, 0.4),
            (3, Barrel, 1, 0.4),
            (3, Skeleton, 0.4, 0.4),
            (3, Barrel, 1, 0.4),
            (3, Ghost, 1, 0.4),
            (3, Skeleton, 0.4, 0.4),
            (5, Barrel, 1, 0.4))),
        ('level7.ogg', (
            (3, Golem, 1, 15),
            (10, Barrel, 0.2, 0.4),
            (5, Ghost, 0.2, 1),
            (5, Barrel, 0.2, 1),
            (5, Skeleton, 0.2, 1),
            (2, Golem, 1, 1),
            (5, Skeleton, 0.4, 0.4),
            (10, Ghost, 0.2, 1),
            (10, Barrel, 0.5, 0.4),
            (3, Skeleton, 0.4, 0.4),
            (3, Barrel, 1, 0.4),
            (3, Skeleton, 0.4, 0.4),
            (5, Barrel, 0.2, 0.4),
            (7, Ghost, 0.2, 0.4),
            (5, Skeleton, 0.2, 0.4))),
        ('level8.ogg', (
            (2, Golem, 1, 15),
            (3, Golem, 1, 15),
            (10, Barrel, 0.5, 0.4),
            (10, Ghost, 0.5, 0.8),
            (2, Golem, 1, 0.8),
            (20, Barrel, 0.5, 1),
            (2, Golem, 1, 5),
            (10, Ghost, 0.5, 2),
            (5, Skeleton, 0.5, 0.3),
            (10, Ghost, 0.5, 0.3),
            (10, Barrel, 0.4, 0.3),
            (5, Skeleton, 0.1, 0.1),
            (5, Golem, 2, 10),
            (10, Skeleton, 0.5, 2),
            (10, Barrel, 0.7, 0.1),
            (10, Golem, 2, 8),
            (10, Ghost, 0.5, 1),
            (10, Skeleton, 0.1, 0.5),
            (5, Golem, 1, 15),
            (10, Barrel, 0.7, 1),
            (20, Skeleton, 0.5, 2),
            (10, Ghost, 0.5, 2),
            (10, Golem, 1, 15)))]
    full_size_decoration = ['assets/level/decoration/castle.png', 'assets/level/decoration/Trforrest.png']

    def __init__(self):
        super(Level1, self).__init__()
