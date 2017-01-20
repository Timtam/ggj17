#/usr/bin/env python2
import sys, pygame

from commons import *
from button import *

class Main:
	def __init__(self, width = 600, height = 480):
		pygame.init()
		get_common().get_bass().Init()
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((width, height))
		self.button = Button('test', 250, 100, self.button_clicked)
		pygame.display.set_caption('Our awesome tower defense game with waves and shit')

	def button_clicked(self):
		print("test")

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
		self.button.update()

	def render(self):
		self.screen.fill((0,0,0))
		ui = get_common().get_ui()
		self.screen.blit(ui.draw_panel_border(100, 100), (100, 100))
		self.button.draw(self.screen)
		pygame.display.flip()

if __name__ == '__main__':
	main = Main()
	main.main_loop()
