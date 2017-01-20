#/usr/bin/env python2
import sys, pygame

from commons import *
from Level   import *

class Main:
	def __init__(self, width = 496, height = 496):
		pygame.init()
		self.width  = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.level  = Level(self.screen)
		pygame.display.set_caption('Our awesome tower defense game with waves and shit')

	def main_loop(self):
		while True:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.stop()
				self.handle_ev(event)
			self.update()
			self.render()

	def stop(self):
		pygame.quit()
		sys.exit()

	def handle_ev(self, event):
		pass

	def update(self):
		pass

	def render(self):
		self.screen.fill((0,0,0))
		ui = get_common().get_ui()
		self.screen.blit(ui.draw_panel_border(100, 100), (100, 100))
		self.level.render()
		pygame.display.flip()

if __name__ == '__main__':
	main = Main()
	main.main_loop()
