import pygame

from commons import *
from button import *

class MainMenu:
	def __init__(self, screen):
		self.screen = screen
		self.buttons = []
		self.buttons.append(Button('Neues Spiel', (self.screen.get_width() - 190) / 2, 300, self.new_game_button_clicked))
		self.buttons.append(Button('Beenden', (self.screen.get_width() - 190) / 2, 350, self.exit_button_clicked))

	def new_game_button_clicked(self):
		pass

	def exit_button_clicked(self):
		get_common().get_main().stop()

	def handle_ev(self, event):
		pass

	def update(self):
		for button in self.buttons:
			button.update()

	def render(self):
		for button in self.buttons:
			button.draw(self.screen)
