from Field import Field
import pygame

class Level:
	def __init__(self, screen):
		self.level       = [(0,8), (1,8), (2,8), (3,8), (4,8), (5,8), (6,8), (7,8), (8,8), (9,8), (10,8), (11,8), (12,8), (13,8), (14,8), (15,8)]
		self.grid        = []
		self.gridsize    = 16
		self.spriteSize  = 32
		self.grassSprite = pygame.image.load('assets/ui/gras.png')
		self.waySprite   = pygame.image.load('assets/ui/erde.png') 
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
				if self.grid[i][j].getType() == 0:
					self.screen.blit(self.grassSprite, (i * self.spriteSize, j * self.spriteSize))
				else:
					self.screen.blit(self.waySprite, (i * self.spriteSize, j * self.spriteSize))
		
	