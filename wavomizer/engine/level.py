import random
import pygame

from ..commons import *
from ..constants import *
from .field import Field

class Level(object):
    way = []
    waves = []
    possible_flowers = []
    possible_decoration = []
    full_size_decoration = []

    def __init__(self):
        self.flowers = []
        for i in range(random.randint(15, 25)):
            self.flowers.append(random.choice(self.possible_flowers))
        self.decoration = []
        for i in range(random.randint(3, 8)):
            self.decoration.append(random.choice(self.possible_decoration))
        self.grid = None
        self.enemies = []
        self.towers = []
        self.way.reverse()

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
    def get_towers(self):
        return self.towers

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
                self.grid[x].append(field)
        return self.grid

    def draw(self):
        ground_layer = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA)
        enemy_layer = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA)
        tower_layer = pygame.Surface((GRID_PIXEL_SIZE, GRID_PIXEL_SIZE), pygame.SRCALPHA)
        grid = self.get_grid()
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                ground_layer.blit(grid[x][y].draw(), (x * TILE_SIZE, y * TILE_SIZE))
        for enemy in self.get_enemies():
            enemy.render(enemy_layer)
        for tower in self.get_towers():
            tower.render(tower_layer)
        ground_layer.blit(enemy_layer, (0, 0))
        ground_layer.blit(tower_layer, (0, 0))
        for decoration in self.full_size_decoration:
            ground_layer.blit(get_common().get_image(decoration), (0, 0))
        return ground_layer

    def update(self, game_screen):
        for enemy in self.get_enemies():
            enemy.update(game_screen)
        for tower in self.get_towers():
            tower.update(game_screen)

    def add_tower(self, tower):
        self.towers.append(tower)
        # sort by y coordinate for rendering
        self.towers.sort(key = lambda tower: tower.tile[1])
    def remove_tower(self, tower):
        self.towers.remove(tower)
    def get_tower_on_tile(self, tile_x, tile_y):
        for tower in self.get_towers():
            if tower.tile == (tile_x, tile_y):
                return tower
        return None

    def add_enemy(self, enemy):
        self.enemies.append(enemy)
    def remove_enemy(self, enemy):
        self.enemies.remove(enemy)
    def get_enemies_on_tile(self, tile_x, tile_y):
        enemies = []
        for enemy in self.get_enemies():
            if enemy.tile == (tile_x, tile_y):
                enemies.append(enemy)
        return enemies

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
