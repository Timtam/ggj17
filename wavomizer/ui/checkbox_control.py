import pygame

from ..commons import *
from ..constants import *
from .control import Control

class CheckboxControl(Control):
    def __init__(self, left, top, callback = None):
        super(CheckboxControl, self).__init__(pygame.Rect(left, top, 32, 32))
        self.set_state(CHECKBOX_UNCHECKED)
        self.callback = callback
        self.was_clicked = False

    def set_state(self, state):
        self.state = state
        self.surface = get_common().get_ui().draw_checkbox(self.state)
    def get_state(self):
        return self.state

    def _update(self):
        lmb, mmb, rmb = pygame.mouse.get_pressed()
        mx, my = pygame.mouse.get_pos()
        if self.was_clicked and not lmb:
            play_sound_fx('assets/sound/ui/release.ogg')
            self.was_clicked = False
        if lmb and not self.was_clicked and self.rect.collidepoint(mx, my):
            if self.state == CHECKBOX_UNCHECKED:
                self.set_state(CHECKBOX_CHECKED)
            elif self.state == CHECKBOX_CHECKED or self.state == CHECKBOX_HALF_CHECKED:
                self.set_state(CHECKBOX_UNCHECKED)
            play_sound_fx('assets/sound/ui/click.ogg')
            self.was_clicked = True
            if self.callback != None:
                self.callback(self)
