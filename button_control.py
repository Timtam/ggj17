import pygame

from commons import *
from control import Control
from text_control import TextControl

class ButtonControl(Control):
	def __init__(self, left, top, text, callback, width = 190):
		super(ButtonControl, self).__init__(pygame.Rect(left, top, width, 32))
		self.state = 0
		self.enabled = True
		self.callback = callback
		self.surface = self.ui.draw_button(self.rect.width, self.state)
		self.text = TextControl(0, 0, text)
		self.add_child_control(self.text, center = True)

	def _update(self):
		if not self.enabled: return
		lmb, mmb, rmb = pygame.mouse.get_pressed()
		if self.state == 1 and not lmb:
			self.state = 0
			self.surface = self.ui.draw_button(self.rect.width, self.state)
			self.text.rect.top -= 4
			play_sound_fx('assets/sound/ui/switch28.ogg')
			self.callback()
		if self.state == 0 and lmb:
			mx, my = pygame.mouse.get_pos()
			if (self.rect.collidepoint(mx, my)):
				self.state = 1
				self.surface = self.ui.draw_button(self.rect.width, self.state)
				self.text.rect.top += 4
				play_sound_fx('assets/sound/ui/switch26.ogg')
