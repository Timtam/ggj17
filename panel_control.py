import pygame

from commons import *
from control import Control

class PanelControl(Control):
    def __init__(self, left, top, width, height, border = True):
        super(PanelControl, self).__init__(pygame.Rect(left, top, width, height))
        self.ui = get_common().get_ui()
        if border:
            self.surface = self.ui.draw_panel_border(self.rect.width, self.rect.height)
        else:
            self.surface = self.ui.draw_panel_full(self.rect.width, self.rect.height)
