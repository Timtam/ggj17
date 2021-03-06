import pygame

from ..commons import *
from .control import Control
from ..towers.water_tower import WaterTower
from ..towers.sound_tower import SoundTower
from ..towers.light_tower import LightTower

class TowerSelectControl(Control):
    def __init__(self, centerx, centery, level):
        super(TowerSelectControl, self).__init__(pygame.Rect(centerx - 32, centery - 32, 64, 64))
        self.level = level
        self.enabled = False
        self.selected_tower = None
        self.background = get_common().get_image('assets/ui/tower_select.png')
        self.towers = []
        self.towers.append(get_common().get_image('assets/level/towers/watertower.png'))
        self.towers.append(get_common().get_image('assets/level/towers/soundtower.png'))
        self.towers.append(get_common().get_image('assets/level/towers/lighttower.png'))
        self.current_panel = None
        self.ui = get_common().get_ui()
        self.cash_icon = get_common().get_image('assets/ui/crystal.png')
        self.tower_classes = [WaterTower, SoundTower, LightTower]
        self.tooltip_panels = []
        font = get_common().get_font()
        font_small = get_common().get_font_small()
        small_space_width,_ = font_small.size(' ')
        for i in range(3):
            panel = self.ui.draw_panel_border(440, 120)
            tower = self.tower_classes[i]
            text_width, text_height = font.size(tower.name)
            cost_x = text_width + 52
            panel.blit(font.render(tower.name, 0, (0, 0, 0)), (10, 10))
            panel.blit(self.cash_icon, (20 + text_width, 4))
            y = 10 + text_height
            x = 10
            text_height = 0
            for word in tower.description.split(' '):
                text_width, text_height = font_small.size(word)
                if x + text_width >= 430:
                    x = 10
                    y += text_height
                panel.blit(font_small.render(word + ' ', 0, (0, 0, 0)), (x, y))
                x += text_width + small_space_width
            y += text_height
            text_width, text_height = font_small.size('Effect: ')
            panel.blit(font_small.render('Effect: ', 0, (0, 0, 0)), (10, y))
            x = 10 + text_width
            for part in tower.effect_desc:
                color = (0, 0, 0)
                if part[0] == '[':
                    part = str(tower.effect_value)
                    color = (0, 127, 127)
                text_width, text_height = font_small.size(part)
                if x + text_width >= 430:
                    x = 10
                    y += text_height
                panel.blit(font_small.render(part, 0, color), (x, y))
                x += text_width
            self.tooltip_panels.append((panel, cost_x, tower.cost))
        self.lmb_down = False

    def enable(self):
        self.enabled = True
        self.lmb_down = False
        self.selected_tower = None
        self.tower_rects = []
        rect = pygame.Rect(0, 0, self.towers[0].get_width(), self.towers[0].get_height())
        rect.centerx = self.rect.centerx
        rect.bottom = self.rect.top + 25
        self.tower_rects.append(rect)
        rect = pygame.Rect(0, 0, self.towers[1].get_width(), self.towers[1].get_height())
        rect.centerx = self.rect.left + 5
        rect.bottom = self.rect.bottom - 5
        self.tower_rects.append(rect)
        rect = pygame.Rect(0, 0, self.towers[2].get_width(), self.towers[2].get_height())
        rect.centerx = self.rect.right - 5
        rect.bottom = self.rect.bottom - 5
        self.tower_rects.append(rect)

    def _draw(self, screen):
        if not self.enabled: return
        screen.blit(self.background, self.rect)
        for i in range(0,3):
            screen.blit(self.towers[i], self.tower_rects[i])
        if self.current_panel != None:
            mx, my = pygame.mouse.get_pos()
            font = get_common().get_font()
            color = (0, 127, 0)
            if self.level.cash < self.current_panel[2]:
                color = (255, 0, 0)
            screen.blit(self.current_panel[0], (mx, my))
            screen.blit(font.render(str(self.current_panel[2]), 0, color), (mx + self.current_panel[1], my + 10))

    def _update(self):
        if not self.enabled: return
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        if lmb:
            for i in range(3):
                if self.tower_rects[i].collidepoint(mx, my):
                    if self.tower_classes[i].cost <= self.level.cash:
                        self.selected_tower = self.tower_classes[i]
            if not self.rect.collidepoint(mx, my):
                self.lmb_down = True
        elif self.lmb_down:
            self.enabled = False
            self.lmb_down = False
        else:
            self.current_panel = None
            for i in range(3):
                if self.tower_rects[i].collidepoint(mx, my):
                    self.current_panel = self.tooltip_panels[i]
