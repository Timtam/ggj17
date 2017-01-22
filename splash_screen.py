import pygame
import time

from commons import *
from controls import *

class SplashScreen:
	def __init__(self, screen):
		self.screen = screen
		self.splash = pygame.transform.scale(get_common().get_image('assets/ui/splash-16by9.png'), self.screen.get_size())
		self.start_time = time.time()

	def leave(self): pass
	def handle_ev(self, event): pass
	def update(self):
		if (time.time() - self.start_time) >= 2.5:
			get_common().get_main().change_view('MainMenu')
	def render(self):
		self.screen.blit(self.splash, (0, 0))
