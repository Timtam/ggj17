import pygame

from commons import *
from control import Control

class ButtonControl(Control):
	def __init__(self, left, top, text, callback, width = 190):
		super(ButtonControl, self).__init__(pygame.Rect(left, top, width, 32))
		self.state = 0
		self.enabled = True
		self.callback = callback
		self.text = text

	def update(self):
		if not self.enabled: return
		lmb, mmb, rmb = pygame.mouse.get_pressed()
		if self.state == 1 and not lmb:
			self.state = 0
			self.callback()
			return
		if self.state == 0 and lmb:
			mx, my = pygame.mouse.get_pos()
			if (self.rect.collidepoint(mx, my)):
				self.state = 1
				channel = get_common().get_bass().StreamCreateFile(False, 'assets/sound/ui/switch26.ogg').Channel
				channel.SetAttribute(BASS_ATTRIB_VOL, 0.5)
				channel.Play()

	def draw(self, screen):
		surface = self.ui.draw_button(self.rect.width, self.state)
		screen.blit(surface, self.rect)
		font = get_common().get_font()
		tw, th = font.size(self.text)
		ts = font.render(self.text, 0, (0, 0, 0))
		if self.state == 1:
			th -= 8
		screen.blit(ts, (self.rect.centerx - tw / 2, self.rect.centery - th / 2))
