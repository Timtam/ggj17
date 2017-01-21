from Field import Field
import pygame

class Level:
	def __init__(self, screen):
		self.level       = [(2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (11, 1), (12, 1), (13, 1), (14, 1), (15, 1),
						    (2, 2), (6, 2), (11, 2),
						    (2, 3), (3, 3), (6, 3), (7, 3), (11, 3), (12, 3),
						    (3, 4), (7, 4), (12, 4),
						    (3, 5), (7, 5), (8, 5), (12, 5)]
		self.grid        = []
		self.gridsize    = 16
		self.spriteSize  = 32
		self.screen      = screen
		
		for i in range(self.gridsize):
			self.grid.append([])
			for j in range(self.gridsize):
				self.grid[i].append(Field(0))
				
		for field in self.level:
			self.grid[field[0]][field[1]] = Field(1)
	

	def leave(self):
		pass

	def render(self):
		for i in range(self.gridsize):
			for j in range(self.gridsize):
				self.screen.blit(self.grid[i][j].render(), (i * self.spriteSize + (self.screen.get_width() / 2) - ((self.gridsize * self.spriteSize) / 2), j * self.spriteSize))
		
	def handle_ev(self, event):
		if event.type == pygame.MOUSEBUTTONUP:
			pos = pygame.mouse.get_pos()
			i = (pos[0] - (self.screen.get_width() / 2) + ((self.gridsize * self.spriteSize) / 2)) / self.spriteSize
			j = pos[1] / self.spriteSize
			print i
			print j
			if not ( i < 0 or i > (self.gridsize - 1) or j < 0 or j > (self.gridsize - 1) ):
				self.grid[i][j].setTower(1)
	
	def update(self):
		pass