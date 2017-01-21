import tower
import pygame

class WaterTower(tower.Tower):
	def __init__(self):
		tower.Tower.__init__(self)
		self.EffectValue=0.3 # in seconds
		self.EffectType=tower.EFFECT_TYPE_STOP|tower.EFFECT_TYPE_ALL|tower.EFFECT_TYPE_STRAIGHT
		self.Speed=12
		self.Sprite = pygame.image.load('assets/level/towers/watertower.png')
