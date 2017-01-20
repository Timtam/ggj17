import pygame

from commons import *

class Button:
	def __init__(self, text, left, top, callback):
		self.ui = get_common().get_ui()
		self.top = top
		self.left = left
		self.state = 0
		self.enabled = True
		self.height = 50
		self.width = 190
		self.callback = callback

	def update(self):
		if not self.enabled: return
		lmb, mmb, rmb = pygame.mouse.get_pressed()
		if self.state == 1 and not lmb:
			self.state = 0
			self.callback()
			return
		if self.state == 0 and lmb:
			mx, my = pygame.mouse.get_pos()
			if (mx >= self.left and mx <= self.left + self.width and my >= self.top and my <= self.top + self.height):
				self.state = 1
				get_common().get_bass().StreamCreateFile(False, 'assets/sound/ui/switch26.ogg').Channel.Play()

	def draw(self, screen):
		surface = self.ui.draw_button(self.width, self.state)
		screen.blit(surface, (self.left, self.top))
