import pygame

from commons import *
from controls import *

class OptionsScreen:
	def __init__(self, screen):
		self.screen = screen
		self.controls = []
		self.controls.append(PanelControl((self.screen.get_width() - 350) / 2, 200, 350, 350))
		self.controls.append(ButtonControl((self.screen.get_width() - 310) / 2, 400, 'Abbrechen', self.cancel_clicked, 150))
		self.controls.append(ButtonControl((self.screen.get_width() - 310) / 2 + 160, 400, 'Speichern', self.save_clicked, 150))

	def cancel_clicked(self):
		pass
	def save_clicked(self):
		pass

	def handle_ev(self, event):
		pass

	def update(self):
		for control in self.controls:
			control.update()

	def render(self):
		for control in self.controls:
			control.draw(self.screen)
