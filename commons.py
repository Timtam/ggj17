import pygame
from Bass4Py.Bass4Py import *

from ui import *
from options import *
import platform

class Commons:
	def __init__(self):
		pass

	def load(self, main):
		self.main = main
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.ui = UI()
		self.options = Options()
		self.options.save()
		if platform.system()=="Windows":
			basspath=('bass_x64.dll' if sys.maxsize>2**32 else 'bass.dll')
		else:
			basspath=('libbass_x64.so' if sys.maxsize>2**32 else 'libbass.so')
		self.bass = BASS(basspath, True)
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

from util import *
