import pygame

from ui import *

class commons:
	def __init__(self):
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.ui = UI()

	def get_font(self):
		return self.font
	def get_ui(self):
		return self.ui

def get_common():
	try:
		return _commons_inst
	except UnboundLocalError:
		_commons_inst = commons()
		return _commons_inst
