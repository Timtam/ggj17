import pygame

from .. import constants

class UI:
    def __init__(self):
        sprite_sheet = pygame.image.load('assets/ui/ui.png')
        self.tower_select = pygame.image.load('assets/ui/tower_select.png')
        color_off = 18 # 6: yellow, 12: green, 18: orange, 24: blue
        # load panel sprites
        self.panel_border = []
        self.panel_full = []
        self.button_down = []
        self.button_up = []
        self.button_disabled = []
        self.slider_horizontal = []
        self.checkbox = []
        for x in range(0,3):
            borders = []
            full = []
            for y in range(0,3):
                b = pygame.Surface((16, 16), pygame.SRCALPHA)
                b.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + x), 18 * (8 + y), 16, 16))
                borders.append(b)
                f = pygame.Surface((16, 16), pygame.SRCALPHA)
                f.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + x), 18 * (5 + y), 16, 16))
                full.append(f)
            self.panel_border.append(borders)
            self.panel_full.append(full)
            up = pygame.Surface((16, 16), pygame.SRCALPHA)
            up.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + x), 18 * 1, 16, 16))
            self.button_up.append(pygame.transform.scale(up, (32, 32)))
            down = pygame.Surface((16, 16), pygame.SRCALPHA)
            down.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + 3 + x), 18 * 1, 16, 16))
            self.button_down.append(pygame.transform.scale(down, (32, 32)))
            slider = pygame.Surface((16, 16), pygame.SRCALPHA)
            slider.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (3 + x), 18 * 8, 16, 16))
            self.slider_horizontal.append(pygame.transform.scale(slider, (32, 32)))
            disabled = pygame.Surface((16, 16), pygame.SRCALPHA)
            disabled.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (3 + x), 18 * 17, 16, 16))
            self.button_disabled.append(pygame.transform.scale(disabled, (32, 32)))
            checkbox = pygame.Surface((16, 16), pygame.SRCALPHA)
            checkbox.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + 3), 18 * (5 + x), 16, 16))
            self.checkbox.append(pygame.transform.scale(checkbox, (32, 32)))
        slider = pygame.Surface((16, 16), pygame.SRCALPHA)
        slider.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + 5), 18 * 6, 16, 16))
        self.slider_horizontal.append(pygame.transform.scale(slider, (32, 32)))

    def draw_panel_full(self, width, height):
        return self.draw_panel(width, height, self.panel_full)
    def draw_panel_border(self, width, height):
        return self.draw_panel(width, height, self.panel_border)
    def draw_panel(self, width, height, sprites):
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        #corners
        surface.blit(sprites[0][0], (0, 0))
        surface.blit(sprites[2][0], (width - 16, 0))
        surface.blit(sprites[0][2], (0, height - 16))
        surface.blit(sprites[2][2], (width - 16, height - 16))
        #borders
        surface.blit(pygame.transform.scale(sprites[1][0], (width - 32, 16)), (16, 0))
        surface.blit(pygame.transform.scale(sprites[1][2], (width - 32, 16)), (16, height - 16))
        surface.blit(pygame.transform.scale(sprites[0][1], (16, height - 32)), (0, 16))
        surface.blit(pygame.transform.scale(sprites[2][1], (16, height - 32)), (width - 16, 16))
        #middle
        surface.blit(pygame.transform.scale(sprites[1][1], (width - 32, height - 32)), (16, 16))
        return surface

    def draw_button(self, width, state):
        if state == 0:
            sprites = self.button_up
        elif state == 1:
            sprites = self.button_down
        elif state == 2:
            sprites = self.button_disabled
        surface = pygame.Surface((width, 32), pygame.SRCALPHA)
        surface.blit(sprites[0], (0,0))
        surface.blit(sprites[2], (width - 32, 0))
        surface.blit(pygame.transform.scale(sprites[1], (width - 64, 32)), (32, 0))
        return surface

    def draw_slider_bar(self, width):
        surface = pygame.Surface((width, 32), pygame.SRCALPHA)
        surface.blit(self.slider_horizontal[0], (0, 0))
        surface.blit(self.slider_horizontal[2], (width - 32, 0))
        surface.blit(pygame.transform.scale(self.slider_horizontal[1], (width - 64, 32)), (32, 0))
        return surface
    def draw_slider(self):
        return self.slider_horizontal[3]

    def draw_checkbox(self, state):
        return self.checkbox[state]
