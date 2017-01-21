import pygame

class Field:
	def __init__(self, screen, ftype):
		self.screen = screen
		self.type  = ftype
		#0 - grass
		if self.type == 0:
			self.sprite = pygame.image.load('assets/ui/gras.png')
		#1 - way
		else:
			self.sprite = pygame.image.load('assets/ui/erde.png')
			
		self.tower = None
		self.enemies=[]
		
	def setTower(self, tower):
		self.tower = tower
		
	def getType(self):
		return self.type
	
	def render(self):
		if self.tower == None:
			return self.sprite
		
		surf = pygame.Surface((32,70), pygame.SRCALPHA)
		surf.blit(self.sprite, (0,38))
		surf.blit(self.tower.render(), (0,0))
		return surf
