import pygame
import time
import random

from field import Field
from enemy import Enemy
from enemies.ghost import Ghost
from enemies.skeleton import Skeleton
from enemies.barrel import Barrel
from enemies.golem import Golem
import tower
from controls import *
from commons import *
from constants import *

class Level:
    def __init__(self, screen):
        self.possible_flowers = [
            (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (8, 0), (9, 0), (10, 0), (11, 0), (12, 0), (13, 0), (14, 0), (15, 0),
            (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (15, 1),
            (0, 2), (1, 2), (2, 2), (3, 2), (4, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2), (10, 2), (11, 2), (12, 2),
            (0, 3), (1, 3), (2, 3), (9, 3), (10, 3),
            (0, 4), (1, 4), (2, 4), (4, 4), (5, 4), (6, 4), (7, 4), (9, 4), (10, 4),
            (0, 5), (1, 5), (2, 5), (4, 5), (5, 5), (6, 5), (7, 5), (10, 5),(11, 5),
            (0, 6), (1, 6), (2, 6), (5, 6), (6, 6), (7, 6), (8, 6), (10, 6), (11, 6), (14, 6), (15, 6),
            (0, 7), (1, 7), (2, 7), (3, 7), (7, 7), (8, 7), (10, 7), (11, 7), (13, 7), (14, 7), (15, 7),
            (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (7, 8), (8, 8), (10, 8), (11, 8), (14, 8), (15, 8),
            (1, 9), (2, 9), (3, 9), (4, 9), (5, 9), (7, 9), (8, 9), (10, 9), (11, 9), (12, 9), (14, 9), (15, 9),
            (2, 10), (7, 10), (8, 10), (10, 10), (11, 10), (12, 10),(14, 10), (15, 10),
            (2, 11), (4, 11), (5, 11), (6, 11), (7, 11), (8, 11), (10, 11), (11, 11), (12, 11), (14, 11), (15, 11),
            (4, 12), (5, 12), (6, 12), (7, 12), (8, 12), (10, 12), (11, 12), (12, 12), (14, 12), (15, 12),
            (2, 13), (3, 13), (4, 13), (5, 13), (6, 13), (7, 13), (8, 13), (14, 13), (15, 13),
            (2, 14), (3, 14), (4, 14), (5, 14), (6, 14), (7, 14), (8, 14), (9, 14), (10, 14), (11, 14), (12, 14), (13, 14), (14, 14), (15, 14),
            (2, 15), (3, 15), (4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15)
        ]
        self.flowers = []
        for i in range(random.randint(15, 25)):
            self.flowers.append(random.choice(self.possible_flowers))

        self.possible_decoration = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1),
            (1, 2), (10, 2),
            (11, 10), (11, 11),
            (1, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (1, 7),
            (1, 8), (2, 8),
            (6, 5),
            (6, 12),
            (5, 13), (6, 13),
            (3, 14), (4, 14), (5, 14), (6, 14), (7, 14)]
        self.decoration = []
        for i in range(random.randint(3, 8)):
            self.decoration.append(random.choice(self.possible_decoration))

        self.way = [
            (1, 12), (2, 12), (3, 12), (3, 11), (3, 10), (4, 10), (5, 10), (6, 10), (6, 9), (6, 8), (6, 7), (5, 7),
            (4, 7), (4, 6), (3, 6), (3, 5), (3, 4), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (8, 4),
            (8, 5), (9, 5), (9, 6), (9, 7), (9, 8), (9, 9), (9, 10), (9, 11), (9, 12), (9, 13), (10, 13),
            (11, 13), (12, 13), (13, 13), (13, 12), (13, 11), (13, 10), (13, 9), (13, 8), (12, 8), (12, 7),
            (12, 6), (13, 6), (13, 5)]
        self.way.reverse()
        self.grid = []
        self.grid_size = 16
        self.tile_size  = 32
        self.screen = screen
        self.field_x = (self.screen.get_width() - self.tile_size * self.grid_size) / 2
        self.field_y = 64
        self.controls = []
        self.cash_icon = get_common().get_image('assets/ui/crystal.png')
        self.enemy_icon = get_common().get_image('assets/ui/sword.png')
        self.time_icon = get_common().get_image('assets/ui/time.png')
        self.health_icon = get_common().get_image('assets/ui/heart.png')
        self.wave_icon = get_common().get_image('assets/ui/enemywave.png')
        self.total_enemies = 0
        self.total_enemies_killed = 0

        self.game_over_panel = None
        self.game_won_panel = None

        self.cash = 300
        self.bgm = None
        self.waves = [
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
        self.current_lives = 20
        self.in_wave = False

        for i in range(self.grid_size):
            self.grid.append([])
            for j in range(self.grid_size):
                self.grid[i].append(Field(self.screen, FIELDTYPE_GRASS, i, j, None, 0))
        latest = self.way[0]
        for i in range(len(self.way)):
            if i == len(self.way) - 1:
                next = self.way[i]
            else:
                next = self.way[i + 1]

            me = self.way[i]

            if latest[0] == self.way[i][0] and self.way[i][0] == self.way[i + 1][0]:
                self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 0, 0)
            elif latest[1] == self.way[i][1] and self.way[i][1] == next[1]:
                self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 0, 90)
            else:
                # dont worry it works - dont touch - dont know how, but its good :)
                # from up to left
                if (me[1] > next[1] and me[0] == next[0] and me[0] > latest[0] and me[1] == latest[1]) or (me[1] > latest[1] and me[0] == latest[0] and me[0] > next[0] and me[1] == next[1]):
                    self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 1, 180)
                # from left to down
                elif (me[0] == next[0] and me[0] > latest[0] and me[1] == latest[1] and me[1] < next[1]) or (me[0] == latest[0] and me[0] > next[0] and me[1] == next[1] and me[1] < latest[1]):
                    self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 1, 270)
                # from right to down
                elif (me[1] == next[1] and me[1] < latest[1] and me[0] == latest[0] and me[0] < next[0]) or (me[1] == latest[1] and me[1] < next[1] and me[0] == next[0] and me[0] < latest[0]):
                    self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 1, 0)
                # from up to right
                elif (me[1] > latest[1] and me[0] == latest[0] and me[1] == next[1] and me[0] < next[0]) or (me[1] > next[1] and me[0] == next[0] and me[1] == latest[1] and me[0] < latest[0]):
                    self.grid[self.way[i][0]][self.way[i][1]] = Field(self.screen, FIELDTYPE_WAY, self.way[i][0], self.way[i][1], 1, 90)

            latest = self.way[i]

        for field in self.decoration:
            self.grid[field[0]][field[1]] = Field(self.screen, FIELDTYPE_DECORATION, field[0], field[1], 0, 0)
        for flower in self.flowers:
            self.grid[flower[0]][flower[1]] = Field(self.screen, FIELDTYPE_FLOWERS, flower[0], flower[1], 0, 0)

        panel_width = self.grid_size * self.tile_size
        panel = PanelControl((self.screen.get_width() - panel_width) / 2, 0, panel_width, self.field_y)
        self.controls.append(panel)
        self.cash_text_control = TextControl(50, 23, '0')
        panel.add_child_control(self.cash_text_control)
        self.enemies_text_control = TextControl(130, 23, '0 / 0')
        panel.add_child_control(self.enemies_text_control)
        self.timer_text_control = TextControl(255, 23, '00:00')
        panel.add_child_control(self.timer_text_control)
        self.health_text_control = TextControl(365, 23, '0')
        panel.add_child_control(self.health_text_control)
        self.wave_text_control = TextControl(445, 23, '0')
        panel.add_child_control(self.wave_text_control)
        self.tower_select = TowerSelectControl(0, 0, self)
        self.controls.append(self.tower_select)

        self.show_tower_panel = False
        self.tower_panel_tower = None
        self.tower_panel = PanelControl(0, 0, 350, 200)
        self.tower_panel.add_child_control(TextControl(10, 15, 'Speed'))
        self.tower_panel.add_child_control(TextControl(10, 55, 'Effect'))
        self.tower_panel.add_child_control(TextControl(10, 95, 'Range'))
        self.upgrade_buttons = []
        self.upgrade_buttons.append(ButtonControl(140, 10, 'Upgrade', self.upgrade_clicked, 100))
        self.upgrade_buttons.append(ButtonControl(140, 50, 'Upgrade', self.upgrade_clicked, 100))
        self.upgrade_buttons.append(ButtonControl(140, 90, 'Upgrade', self.upgrade_clicked, 100))
        self.upgrade_cost_texts = []
        self.upgrade_cost_texts.append(TextControl(280, 15, '0'))
        self.upgrade_cost_texts.append(TextControl(280, 55, '0'))
        self.upgrade_cost_texts.append(TextControl(280, 95, '0'))
        for i in range(3):
            self.tower_panel.add_child_control(self.upgrade_buttons[i])
            self.tower_panel.add_child_control(self.upgrade_cost_texts[i])
        self.sell_button = ButtonControl(10, 158, 'Sell tower', self.sell_clicked, 120)
        self.sell_value_text = TextControl(170, 163, '0')
        self.tower_panel.add_child_control(self.sell_button)
        self.tower_panel.add_child_control(self.sell_value_text)

        self.paused = False
        self.show_pause_panel = False
        self.was_paused = False
        self.pause_start_time = None
        self.pause_panel = PanelControl((self.screen.get_width() - 400) / 2, (self.screen.get_height() - 400) / 2, 400, 400)
        self.pause_panel.add_child_control(TextControl(0, 0, 'Paused'), center = True)
        self.pause_panel.add_child_control(ButtonControl(105, 350, 'Back to main menu', self.back_to_main_clicked))

        self.pause_dim = pygame.transform.scale(get_common().get_image('assets/ui/dim.png'), self.screen.get_size())

        self.current_wave = -1
        self.won = False
        self.game_over = False
        self.start_wave_button = ButtonControl(self.field_x + panel_width + 50, self.field_y + 150, 'Start wave', self.start_wave_clicked)
        self.init_wave(0)

    def leave(self):
        if self.bgm != None:
            self.bgm.Stop()

    def next_wave(self):
        self.init_wave(self.current_wave + 1)

    def init_wave(self, index = 0):
        if self.bgm != None:
            self.bgm.Stop()
        wave = self.waves[index]
        self.current_wave = index
        self.bgm = play_sound_bgm('assets/sound/bgm/' + wave[0])
        self.enemy_types = wave[1]
        self.total_enemies_wave = 0
        self.removed_enemies = 0
        self.all_enemies = []
        for e in self.enemy_types:
            self.total_enemies_wave += e[0]
            for i in range(e[0] - 1):
                self.all_enemies.append((e[1], e[2]))
            if len(e) == 4:
                self.all_enemies.append((e[1], e[3]))
            else:
                self.all_enemies.append((e[1], 0))
        self.total_enemies += self.total_enemies_wave
        self.killed_enemies = 0
        self.enemy_spawn_index = 0
        self.in_wave = False

    def start_wave(self):
        self.in_wave = True
        play_sound_fx('assets/sound/common/level_start.ogg')
        self.next_enemy_spawn = time.time()
        self.wave_started = time.time()

    def start_wave_clicked(self):
        self.start_wave()
    def back_to_main_clicked(self):
        get_common().get_main().change_view('MainMenu')

    def restart_game_clicked(self):
        get_common().get_main().change_view('Level')

    def upgrade_clicked(self, button):
        upgrade = self.upgrade_buttons.index(button)
        cost = self.tower_panel_tower.upgrade_costs[upgrade]
        if cost < self.cash:
            self.tower_panel_tower.upgrade(upgrade)
            self.show_tower_panel = False
    def sell_clicked(self):
        self.show_tower_panel = False
        self.tower_panel_tower.sell()

    def remove_enemy(self, enemy):
        self.removed_enemies += 1
        if enemy.die == DIE_DAMAGE:
            self.total_enemies_killed += 1
            self.killed_enemies += 1
            self.cash += enemy.drop
        elif enemy.die == DIE_SUCCESS:
            self.current_lives -= enemy.damage
        if self.current_lives <= 0:
            if self.bgm != None:
                self.bgm.Stop()
            play_sound_fx('assets/sound/common/game_over.ogg')
            self.paused = True
            self.game_over = True
            self.create_game_end_panel(True)
        elif self.removed_enemies == self.total_enemies_wave:
            play_sound_fx('assets/sound/common/level_win.ogg')
            if self.current_wave < len(self.waves) - 1:
                #20% more cash after every round
                self.cash = int(self.cash * 1.2)
                play_sound_fx("assets/sound/common/coin.ogg")
                self.next_wave()
            else:
                self.create_game_end_panel(False)
                self.paused = True
                self.won = True

    def create_game_end_panel(self, gameover):
        line_height_before = 60
        me = PanelControl((self.screen.get_width() - 400) / 2, (self.screen.get_height() - 400) / 2, 400, 400)
        if gameover:
            tc = TextControl(0, line_height_before, 'GAME OVER')
        else:
            tc = TextControl(0, line_height_before, 'CONGRATULATIONS')
        tc.rect.centerx = 200
        me.add_child_control(tc)

        tower_counter = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid[i][j].tower != None:
                    tower_counter += 1

        tc = TextControl(155, line_height_before + tc.rect.height, 'You reached wave ' + str(self.current_wave + 1) + ' of ' + str(len(self.waves)) + '.' )
        tc.rect.centerx = 200
        line_height_before += tc.rect.height
        me.add_child_control(tc)

        tc = TextControl(155, line_height_before + tc.rect.height, 'You built ' + str(tower_counter) + ' towers' )
        tc.rect.centerx = 200
        line_height_before += tc.rect.height
        me.add_child_control(tc)

        tc = TextControl(155, line_height_before + tc.rect.height, 'and slayed ' + str(self.total_enemies_killed) + " / " + str(self.total_enemies) + ' enemies.' )
        tc.rect.centerx = 200
        line_height_before += tc.rect.height
        me.add_child_control(tc)

        me.add_child_control(ButtonControl(105, 300, 'Back to main menu', self.back_to_main_clicked))
        me.add_child_control(ButtonControl(105, 350, 'Restart game', self.restart_game_clicked))

        if gameover:
            self.game_over_panel = me
        else:
            self.game_won_panel = me

    def render(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.screen.blit(self.grid[i][j].render_underground(), (i * self.tile_size + self.field_x, j * self.tile_size + self.field_y))
                if self.grid[i][j].type == 2:
                    self.screen.blit(self.grid[i][j].render_deco(), (i * self.tile_size + self.field_x, j * self.tile_size + self.field_y))

        self.screen.blit(get_common().get_image('assets/level/decoration/castle.png'), (self.field_x, self.field_y))

        for j in range(self.grid_size):
            for i in range(self.grid_size):
                for enemy in self.grid[i][j].enemies:
                    surf, coord = enemy.render()
                    self.screen.blit(surf, (coord[0] + i * self.tile_size + self.field_x, coord[1] + (j * self.tile_size) + self.field_y))
        for j in range(self.grid_size):
            for i in range(self.grid_size):
                if self.grid[i][j].tower != None:
                    surf, coord, render_above = self.grid[i][j].render_tower_animation()
                    if not render_above:
                        self.screen.blit(surf, (coord[0] + self.field_x + i * self.tile_size, coord[1] + self.field_y + j * self.tile_size))
                    tmpsprite = self.grid[i][j].render_tower()
                    self.screen.blit(tmpsprite, (i * self.tile_size + self.field_x - (tmpsprite.get_width() - self.tile_size) / 2, (j * self.tile_size) - (tmpsprite.get_height() - self.tile_size) + self.field_y))
                    if render_above:
                        self.screen.blit(surf, (coord[0] + self.field_x + i * self.tile_size, coord[1] + self.field_y + j * self.tile_size))
        self.screen.blit(get_common().get_image('assets/level/decoration/Trforrest.png'), (self.field_x, self.field_y))

        self.screen.blit(get_common().get_image('assets/ui/frame.png'), (0, 0))
        for control in self.controls:
            control.draw(self.screen)

        if not self.in_wave:
            self.start_wave_button.draw(self.screen)
        self.screen.blit(self.cash_icon, (self.field_x + 17, 17))
        self.screen.blit(self.enemy_icon, (self.field_x + 97, 17))
        self.screen.blit(self.time_icon, (self.field_x + 217, 17))
        self.screen.blit(self.health_icon, (self.field_x + 327, 17))
        self.screen.blit(self.wave_icon, (self.field_x + 410, 17))
        if self.show_tower_panel:
            self.tower_panel.draw(self.screen)
            if self.upgrade_buttons[0].enabled:
                self.screen.blit(self.cash_icon, (self.tower_panel.rect.x + 250, self.tower_panel.rect.y + 10))
            if self.upgrade_buttons[1].enabled:
                self.screen.blit(self.cash_icon, (self.tower_panel.rect.x + 250, self.tower_panel.rect.y + 50))
            if self.upgrade_buttons[2].enabled:
                self.screen.blit(self.cash_icon, (self.tower_panel.rect.x + 250, self.tower_panel.rect.y + 90))
            self.screen.blit(self.cash_icon, (self.tower_panel.rect.x + 140, self.tower_panel.rect.y + 158))
        if self.paused:
            self.screen.blit(self.pause_dim, (0, 0))
        if self.show_pause_panel:
            self.pause_panel.draw(self.screen)
        if self.game_over:
            self.game_over_panel.draw(self.screen)
        if self.won:
            self.game_won_panel.draw(self.screen)

    def handle_ev(self, event):
        if event.type == pygame.MOUSEBUTTONUP and not self.tower_select.enabled and not self.paused:
            pos = pygame.mouse.get_pos()
            i = (pos[0] - self.field_x) / self.tile_size
            j = (pos[1] - self.field_y) / self.tile_size
            if event.button == 1:
                if not ( i < 0 or i > (self.grid_size - 1) or j < 0 or j > (self.grid_size - 1) ):
                    field = self.grid[i][j]
                    if field.get_type() == FIELDTYPE_GRASS or field.get_type() == FIELDTYPE_FLOWERS:
                        if field.tower == None and not self.show_tower_panel:
                            self.tower_select.rect.centerx = i * self.tile_size + self.field_x + self.tile_size / 2
                            self.tower_select.rect.centery = j * self.tile_size + self.field_y + self.tile_size / 2
                            self.tower_select.enable()
                            self.new_tower_coord = (i, j)
                        elif field.tower != None and not self.show_tower_panel:
                            for u in range(3):
                                self.upgrade_buttons[u].set_text('Upgrade')
                                self.upgrade_buttons[u].enable()
                                self.upgrade_cost_texts[u].set_text(str(field.tower.upgrade_costs[u]))
                            self.tower_panel.reset_child_controls()
                            self.tower_panel.rect.x = i * self.tile_size + self.field_x
                            self.tower_panel.rect.y = j * self.tile_size + self.field_y
                            size = self.grid_size * self.tile_size
                            if self.tower_panel.rect.right > size + self.field_x:
                                self.tower_panel.rect.right = size + self.field_x
                            if self.tower_panel.rect.bottom > size + self.field_y:
                                self.tower_panel.rect.bottom = size + self.field_y
                            self.tower_panel.transform_child_controls()
                            self.show_tower_panel = True
                            self.tower_panel_tower = field.tower
                            can_upgrade = field.tower.can_upgrades()
                            self.sell_value_text.set_text(str(field.tower.get_value()))
                            for u in range(3):
                                if not can_upgrade[u]:
                                    self.upgrade_buttons[u].set_text('Upgraded')
                                    self.upgrade_buttons[u].disable()
                                    self.upgrade_cost_texts[u].set_text('')
                if self.show_tower_panel and not self.tower_panel.rect.collidepoint(*pos):
                    self.show_tower_panel = False

        if event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            if self.paused:
                if self.show_pause_panel:
                    self.was_paused = True
                    self.paused = False
                    self.show_pause_panel = False
            else:
                self.paused = True
                self.pause_start_time = time.time()
                self.show_pause_panel = True
        if self.tower_select.enabled and self.tower_select.selected_tower != None:
            self.tower_select.enabled = False
            i, j = self.new_tower_coord
            tower = self.tower_select.selected_tower
            tower.init()
            self.grid[i][j].set_tower(tower, self.way)

    def update(self):
        if not self.paused:
            if self.was_paused:
                self.was_paused = False
                time_delta = time.time() - self.pause_start_time
                for i in range(self.grid_size):
                    for j in range(self.grid_size):
                        field = self.grid[i][j]
                        if field.tower != None:
                            field.tower.last_fire += time_delta
                        for enemy in field.enemies:
                            enemy.start += time_delta
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.grid[i][j].update_enemies(self)
            for i in range(self.grid_size):
                for j in range(self.grid_size):
                    self.grid[i][j].update_tower(self)
            if self.in_wave and not self.won:
                if time.time() >= self.next_enemy_spawn and len(self.all_enemies) > self.enemy_spawn_index:
                    first_coord = self.way[-1]
                    enemy = self.all_enemies[self.enemy_spawn_index]
                    self.enemy_spawn_index += 1
                    new_enemy = enemy[0]()
                    new_enemy.init()
                    self.grid[first_coord[0]][first_coord[1]].enemies.append(new_enemy)
                    self.next_enemy_spawn += enemy[1]
                wave_time = int(time.time() - self.wave_started)
                s = wave_time % 60
                m = (wave_time - s) / 60
                s = str(s).zfill(2)
                m = str(m).zfill(2)
                self.timer_text_control.set_text(m + ':' + s)
            self.enemies_text_control.set_text(str(self.killed_enemies) + " / " + str(self.total_enemies_wave))
            self.cash_text_control.set_text(str(self.cash))
            self.wave_text_control.set_text(str(self.current_wave + 1) + ' / ' + str(len(self.waves)))
            self.health_text_control.set_text(str(self.current_lives))
        for control in self.controls:
            control.update()
        if not self.in_wave:
            self.start_wave_button.update()
        if self.show_pause_panel:
            self.pause_panel.update()
        if self.show_tower_panel:
            for i in range(3):
                cost = self.tower_panel_tower.upgrade_costs[i]
                if cost < self.cash and self.tower_panel_tower.can_upgrades()[i]:
                    self.upgrade_buttons[i].enable()
                else:
                    self.upgrade_buttons[i].disable()
            self.tower_panel.update()
        if self.game_over:
            self.game_over_panel.update()
        if self.won:
            self.game_won_panel.update()
