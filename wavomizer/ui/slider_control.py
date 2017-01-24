import pygame

from wavomizer.commons import *
from wavomizer.ui.control import Control

class SliderControl(Control):
    def __init__(self, left, top, width, release_callback = None, slider_pos = 1):
        super(SliderControl, self).__init__(pygame.Rect(left, top, width, 32))
        self.surface = self.ui.draw_slider_bar(self.rect.width)
        self.slider_pos = slider_pos
        self.state = 0
        self.release_callback = release_callback

    def _draw(self, screen):
        screen.blit(self.ui.draw_slider(), self.slider_rect)

    def _update(self):
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        if self.state == 0 and lmb and self.rect.collidepoint(mx, my):
            self.state = 1
        if self.state == 1 and not lmb:
            self.state = 0
            if self.release_callback != None:
                self.release_callback()
        if self.state == 1:
            self.slider_pos = min(1, max(0, (float(mx) - 8 - self.rect.x) / (self.rect.width - 32)))
        self.slider_rect = pygame.Rect(self.slider_pos * (self.rect.width - 32) + self.rect.x, self.rect.y, 32, 32)
