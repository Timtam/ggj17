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
        for i in range(3):
            panel = self.ui.draw_panel_border(440, 120)
            tc = self.tower_classes[i]
            tw, th = font.size(tc.name)
            cost_x = tw + 52
            panel.blit(font.render(tc.name, 0, (0, 0, 0)), (10, 10))
            panel.blit(self.cash_icon, (20 + tw, 4))
            y = 30
            for line in tc.description.split('\n'):
                panel.blit(font_small.render(line.strip(), 0, (0, 0, 0)), (10, y))
                y += 20
            y += 10
            tw, th = font_small.size('Effect: ')
            x = 10
            panel.blit(font_small.render('Effect: ', 0, (0, 0, 0)), (x, y))
            x += tw
            for part in tc.effect_desc:
                color = (0, 0, 0)
                if part[0] == '[':
                    part = str(tc().effect_value)
                    color = (0, 127, 127)
                tw, th = font_small.size(part)
                if x + tw >= 430:
                    x = 10
                    y += th
                panel.blit(font_small.render(part, 0, color), (x, y))
                x += tw
            self.tooltip_panels.append((panel, cost_x, tc.cost))
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
                        self.selected_tower = self.tower_classes[i]()
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
