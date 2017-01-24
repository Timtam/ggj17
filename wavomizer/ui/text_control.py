import pygame

from wavomizer.commons import *
from wavomizer.ui.control import Control

class TextControl(Control):
    def __init__(self, left, top, text):
        super(TextControl, self).__init__(pygame.Rect(left, top, 0, 0))
        self.set_text(text)
    def set_text(self, new_text):
        font = get_common().get_font()
        tw, th = font.size(new_text)
        self.rect.width = tw
        self.rect.height = th
        self.surface = font.render(new_text, 0, (0, 0, 0))
