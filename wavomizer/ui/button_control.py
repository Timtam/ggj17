import pygame
import inspect

from ..commons import *
from .control import Control
from .text_control import TextControl

class ButtonControl(Control):
    def __init__(self, left, top, text, callback, width = 190):
        super(ButtonControl, self).__init__(pygame.Rect(left, top, width, 32))
        self.state = 0
        self.enabled = True
        arg_num = len(inspect.getargspec(callback).args)
        if arg_num == 2:
            self.callback = callback
        else:
            def c(s):
                callback()
            self.callback = c
        self.surface = self.ui.draw_button(self.rect.width, self.state)
        self.text = TextControl(0, 0, text)
        self.add_child_control(self.text, center = True)

    def enable(self):
        if not self.enabled:
            self.enabled = True
            self.state = 0
            self.text.rect.top -= 4
            self.refresh_surface()

    def disable(self):
        if self.enabled:
            self.enabled = False
            self.state = 2
            self.text.rect.top += 4
            self.refresh_surface()

    def refresh_surface(self):
        self.surface = self.ui.draw_button(self.rect.width, self.state)

    def set_text(self, text):
        self.reset_child_controls()
        self.text.set_text(text)
        self.transform_child_controls()

    def _update(self):
        if not self.enabled: return
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        if self.state == 1 and not lmb:
            self.state = 0
            self.text.rect.top -= 4
            play_sound_fx('assets/sound/ui/release.ogg')
            self.refresh_surface()
            self.callback(self)
        if self.state == 0 and lmb:
            mx, my = pygame.mouse.get_pos()
            if (self.rect.collidepoint(mx, my)):
                self.state = 1
                self.text.rect.top += 4
                play_sound_fx('assets/sound/ui/click.ogg')
                self.refresh_surface()
