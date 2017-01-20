import pygame
from Bass4Py.Bass4Py import *

from ui import *

BGM_MAX_VOL = 0.20
BGM_FADE_DURATION = 2

class commons:
	def __init__(self):
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.ui = UI()
		self.bass = BASS('bass.dll', True)

	def get_font(self):
		return self.font
	def get_ui(self):
		return self.ui
	def get_bass(self):
		return self.bass

def get_common():
	try:
		return _commons_inst
	except UnboundLocalError:
		_commons_inst = commons()
		return _commons_inst
