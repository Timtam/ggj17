import pygame

from commons import *
from control import Control

class TextControl(Control):
	def __init__(self, left, top, text):
		super(TextControl, self).__init__(pygame.Rect(left, top, 0, 0))
		font = get_common().get_font()
		tw, th = font.size(text)
		self.rect.width = tw
		self.rect.height = th
		self.surface = font.render(text, 0, (0, 0, 0))
