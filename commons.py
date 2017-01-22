import pygame
from Bass4Py.Bass4Py import *

from ui import *
from options import *
import platform

from script import Script

import os.path

class Commons:
	def __init__(self):
		self.image_cache = {}
		self.sound_cache = {}

	def load(self, main):
		self.main = main
		self.font = pygame.font.Font('assets/font/KenPixel.ttf', 14)
		self.font_small = pygame.font.Font('assets/font/KenPixel Nova.ttf', 25)
		self.ui = UI()
		self.options = Options()
		self.options.save()
		if platform.system()=="Windows":
			basspath=os.path.join(Script().Path, ('bass_x64.dll' if sys.maxsize>2**32 else 'bass.dll'))
		else:
			basspath=os.path.joion(Script().Path, ('libbass_x64.so' if sys.maxsize>2**32 else 'libbass.so'))
		self.bass = BASS(basspath, True)
		self.bass.Init()

	def get_font(self):
		return self.font
	def get_font_small(self):
		return self.font_small
	def get_ui(self):
		return self.ui
	def get_bass(self):
		return self.bass
	def get_main(self):
		return self.main
	def get_options(self):
		return self.options
	def get_image(self, filename):
		if filename in self.image_cache:
			return self.image_cache[filename]
		else:
			asset = pygame.image.load(filename)
			self.image_cache[filename] = asset
			return asset

	def get_sound(self, filename, music=False):
		if filename in self.sound_cache:
			return self.sound_cache[filename]
		channel = self.bass.StreamCreateFile(False, filename, 0, 0, BASS_SAMPLE_LOOP if music==True else 0).Channel
		self.sound_cache[filename] = channel
		return channel

instance = None
def get_common():
	global instance
	if instance == None:
		instance = Commons()
	return instance

from util import *
