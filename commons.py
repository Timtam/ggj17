import pygame
from Bass4Py.Bass4Py import *

from ui import *
from options import *

class Commons:
	def __init__(self):
		pass

	def load(self, main):
		self.main = main
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.ui = UI()
		self.options = Options()
		self.options.save()
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
	def get_options(self):
		return self.options

instance = None
def get_common():
	global instance
	if instance == None:
		instance = Commons()
	return instance
