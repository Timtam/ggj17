import pygame

class Field:
	def __init__(self, ftype):
		self.type  = ftype
		#0 - grass
		if self.type == 0:
			self.sprite = pygame.image.load('assets/ui/gras.png')
		#1 - way
		else:
			self.sprite = pygame.image.load('assets/ui/erde.png')
			
		self.tower = None
		
	def setTower(self, tower):
		self.sprite = pygame.image.load('assets/ui/erde.png')
		
	def getType(self):
		return self.type
	
	def render(self):
		return self.sprite