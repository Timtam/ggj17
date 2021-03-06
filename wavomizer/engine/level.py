import random
import pygame

from ..commons import *
from ..constants import *
from .field import Field

class Level(object):
    def __init__(self):
        self.grid = None
        self.enemies = []
        self.enemy_search_dict = {}

        self.way = []
        self.possible_flowers = []
        self.possible_decoration = []
        self.waves = []
        self.full_size_decoration = []
        self.towerless_fields = []

    def init(self):
        self.flowers = []
        for i in range(random.randint(15, 25)):
            self.flowers.append(random.choice(self.possible_flowers))
        self.decoration = []
        for i in range(random.randint(3, 8)):
            self.decoration.append(random.choice(self.possible_decoration))
        self.way.reverse()
        self.ground_layer = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA).convert()
        self.deco_layer = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA).convert_alpha()
        for decoration in self.full_size_decoration:
            self.deco_layer.blit(get_common().get_image(decoration), (0, 0))

    def get_way(self):
        return self.way
    def get_waves(self):
        return self.waves
    def get_possible_flowers(self):
        return self.possible_flowers
    def get_possible_decoration(self):
        return self.possible_decoration

    def get_flowers(self):
        return self.flowers
    def get_decoration(self):
        return self.decoration

    def get_grid(self):
        if self.grid == None:
            return self.generate_grid()
        else:
            return self.grid

    def get_enemies(self):
        return self.enemies

    def generate_grid(self):
        self.grid = []
        for x in range(GRID_SIZE):
            self.grid.append([])
            for y in range(GRID_SIZE):
                if (x, y) in self.get_way():
                    field = self.create_way_field(x, y)
                elif (x, y) in self.get_decoration():
                    field = Field(self, FIELDTYPE_DECORATION, x, y, None, 0)
                elif (x, y) in self.get_flowers():
                    field = Field(self, FIELDTYPE_FLOWERS, x, y, None, 0)
                else:
                    field = Field(self, FIELDTYPE_GRASS, x, y, None, 0)
                if (x, y) in self.get_towerless_fields():
                    field.forbid_tower()

                self.grid[x].append(field)
                self.ground_layer.blit(field.draw(), (x * TILE_SIZE, y * TILE_SIZE))
        return self.grid

    def draw(self):
        surface = self.ground_layer.copy()
        for enemy in self.get_enemies():
            enemy.render(surface)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                field = self.grid[x][y]
                if field.tower != None:
                    field.tower.render(surface)
        surface.blit(self.deco_layer, (0, 0))
        return surface

    def update(self, game_screen):
        self.enemy_search_dict.clear()
        for enemy in self.get_enemies():
            enemy.update(game_screen)
            if not enemy.tile in self.enemy_search_dict:
                self.enemy_search_dict[enemy.tile] = [enemy]
            else:
                self.enemy_search_dict[enemy.tile].append(enemy)
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                field = self.grid[x][y]
                if field.tower != None:
                    field.tower.update(game_screen)

    def add_tower(self, tower, x, y):
        tower.set_tile(x, y)
        self.get_grid()[x][y].tower = tower
    def remove_tower(self, tower):
        self.get_grid()[tower.tile[0]][tower.tile[1]].tower = None

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
    def get_enemies_on_tile(self, tile_x, tile_y):
        tile = (tile_x, tile_y)
        if tile in self.enemy_search_dict:
            return self.enemy_search_dict[(tile_x, tile_y)]
        else:
            return []

    def create_way_field(self, x, y):
        way = self.get_way()
        if (x - 1, y) in way and (x, y - 1) in way: # left, up
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_CURVE, 180)
        elif (x - 1, y) in way and (x, y + 1) in way: # left, down
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_CURVE, 270)
        elif (x + 1, y) in way and (x, y - 1) in way: # right, up
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_CURVE, 90)
        elif (x + 1, y) in way and (x, y + 1) in way: # right, down
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_CURVE, 0)
        elif (x - 1, y) in way or (x + 1, y) in way: # left, right
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_STRAIGHT, 90)
        elif (x, y - 1) in way or (x, y + 1) in way: # up, down
            return Field(self, FIELDTYPE_WAY, x, y, WAYTYPE_STRAIGHT, 0)

    def get_towerless_fields(self):
        return self.towerless_fields

    def count_towers(self):
        count=0
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if self.grid[x][y].tower != None:
                    count+=1

        return count