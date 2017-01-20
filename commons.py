import pygame
from Bass4Py.Bass4Py import *

from ui import *

BGM_MAX_VOL = 0.20
BGM_FADE_DURATION = 2

class commons:
	def __init__(self):
		pass

	def load(self, main):
		self.main = main
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.ui = UI()
		self.bass = BASS('bass.dll', True)
		self.bass.Init()

	def get_font(self):
		return self.font
	def get_ui(self):
		return self.ui
	def get_bass(self):
		return self.bass
	def get_main(self):
		return self.main

instance = None
def get_common():
	global instance
	if instance == None:
		instance = commons()
	return instance
