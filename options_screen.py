import pygame

from commons import *
from controls import *

class OptionsScreen:
	def __init__(self, screen):
		self.screen = screen
		self.controls = []
		panel = PanelControl((self.screen.get_width() - 350) / 2, 200, 350, 350)
		self.controls.append(panel)
		panel.add_child_control(ButtonControl(20, 300, 'Abbrechen', self.cancel_clicked, 150))
		panel.add_child_control(ButtonControl(180, 300, 'Speichern', self.save_clicked, 150))

	def cancel_clicked(self):
		get_common().get_main().change_view('MainMenu')
	def save_clicked(self):
		options = get_common().get_options()
		get_common().get_main().change_view('MainMenu')

	def handle_ev(self, event):
		pass

	def update(self):
		for control in self.controls:
			control.update()

	def render(self):
		for control in self.controls:
			control.draw(self.screen)
