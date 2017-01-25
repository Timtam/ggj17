import pygame
import random

from ..commons import *
from ..constants import *
from ..ui.controls import *
from ..levels.level1 import Level1
from .field import Field
from .tower import Tower
from .enemy import Enemy
from ..enemies.ghost import Ghost
from ..enemies.skeleton import Skeleton
from ..enemies.barrel import Barrel
from ..enemies.golem import Golem
from . import game_time

class GameScreen:
    def __init__(self, screen):
        self.screen = screen
        self.level = Level1()
        self.grid = self.level.generate_grid()
        self.field_x = (self.screen.get_width() - GRID_PIXEL_SIZE) / 2
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

        self.current_lives = 20
        self.in_wave = False

        panel_width = GRID_PIXEL_SIZE
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

        # convert frame to non-alpha surface to speed up blitting (this single blit takes about 0.02 seconds if frame is a surface with transparency)
        self.frame = get_common().get_image('assets/ui/frame.png').convert()

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
        wave = self.level.get_waves()[index]
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
        self.next_enemy_spawn = game_time.time()
        self.wave_started = game_time.time()

    def start_wave_clicked(self):
        self.start_wave()
    def back_to_main_clicked(self):
        get_common().get_main().change_view('MainMenu')

    def restart_game_clicked(self):
        get_common().get_main().change_view('GameScreen')

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
            if self.current_wave < len(self.level.waves) - 1:
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

        tower_counter = len(self.level.get_towers())

        tc = TextControl(155, line_height_before + tc.rect.height, 'You reached wave ' + str(self.current_wave + 1) + ' of ' + str(len(self.level.waves)) + '.' )
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
        self.screen.blit(self.frame, (0, 0))
        self.screen.blit(self.level.draw(), (self.field_x, self.field_y))

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
            i = (pos[0] - self.field_x) / TILE_SIZE
            j = (pos[1] - self.field_y) / TILE_SIZE
            if event.button == 1:
                if not ( i < 0 or i > (GRID_SIZE - 1) or j < 0 or j > (GRID_SIZE - 1) ):
                    tile = self.level.get_grid()[i][j]
                    tower = self.level.get_tower_on_tile(i, j)
                    if tile.get_type() == FIELDTYPE_GRASS or tile.get_type() == FIELDTYPE_FLOWERS:
                        if tower == None and not self.show_tower_panel:
                            self.tower_select.rect.centerx = i * TILE_SIZE + self.field_x + TILE_SIZE / 2
                            self.tower_select.rect.centery = j * TILE_SIZE + self.field_y + TILE_SIZE / 2
                            self.tower_select.enable()
                            self.new_tower_coord = (i, j)
                        elif tower != None and not self.show_tower_panel:
                            for u in range(3):
                                self.upgrade_buttons[u].set_text('Upgrade')
                                self.upgrade_buttons[u].enable()
                                self.upgrade_cost_texts[u].set_text(str(tower.upgrade_costs[u]))
                            self.tower_panel.reset_child_controls()
                            self.tower_panel.rect.x = i * TILE_SIZE + self.field_x
                            self.tower_panel.rect.y = j * TILE_SIZE + self.field_y
                            if self.tower_panel.rect.right > GRID_PIXEL_SIZE + self.field_x:
                                self.tower_panel.rect.right = GRID_PIXEL_SIZE + self.field_x
                            if self.tower_panel.rect.bottom > GRID_PIXEL_SIZE + self.field_y:
                                self.tower_panel.rect.bottom = GRID_PIXEL_SIZE + self.field_y
                            self.tower_panel.transform_child_controls()
                            self.show_tower_panel = True
                            self.tower_panel_tower = tower
                            can_upgrade = tower.can_upgrades()
                            self.sell_value_text.set_text(str(tower.get_value()))
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
                    self.paused = False
                    game_time.resume_time()
                    self.show_pause_panel = False
            else:
                self.paused = True
                game_time.pause_time()
                self.show_pause_panel = True
        if self.tower_select.enabled and self.tower_select.selected_tower != None:
            self.tower_select.enabled = False
            i, j = self.new_tower_coord
            tower = self.tower_select.selected_tower
            tower = tower(self.level)
            tower.init(i, j)
            self.level.add_tower(tower)

    def update(self):
        if not self.paused:
            self.level.update(self)
            if self.in_wave and not self.won:
                if game_time.time() >= self.next_enemy_spawn and len(self.all_enemies) > self.enemy_spawn_index:
                    first_coord = self.level.get_way()[-1]
                    enemy = self.all_enemies[self.enemy_spawn_index]
                    self.enemy_spawn_index += 1
                    new_enemy = enemy[0](self.level)
                    new_enemy.init(first_coord[0], first_coord[1])
                    self.level.add_enemy(new_enemy)
                    self.next_enemy_spawn += enemy[1]
                wave_time = int(game_time.time() - self.wave_started)
                s = wave_time % 60
                m = (wave_time - s) / 60
                s = str(s).zfill(2)
                m = str(m).zfill(2)
                self.timer_text_control.set_text(m + ':' + s)
            self.enemies_text_control.set_text(str(self.killed_enemies) + " / " + str(self.total_enemies_wave))
            self.cash_text_control.set_text(str(self.cash))
            self.wave_text_control.set_text(str(self.current_wave + 1) + ' / ' + str(len(self.level.get_waves())))
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
                if cost <= self.cash and self.tower_panel_tower.can_upgrades()[i]:
                    self.upgrade_buttons[i].enable()
                else:
                    self.upgrade_buttons[i].disable()
            self.tower_panel.update()
        if self.game_over:
            self.game_over_panel.update()
        if self.won:
            self.game_won_panel.update()
