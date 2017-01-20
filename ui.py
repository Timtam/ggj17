import pygame

class UI:
	def __init__(self):
		sprite_sheet = pygame.image.load('assets/ui/ui.png')
		color_off = 6 # 6: yellow, 12: green, 18: orange, 24: blue
		# load panel sprites
		self.panel_border = []
		self.panel_full = []
		for x in range(0,3):
			borders = []
			full = []
			for y in range(0,3):
				b = pygame.Surface((16, 16), pygame.SRCALPHA)
				b.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + x), 18 * (8 + y), 16, 16))
				borders.append(b)
				f = pygame.Surface((16, 16), pygame.SRCALPHA)
				f.blit(sprite_sheet, (0, 0), pygame.Rect(18 * (color_off + x), 18 * (5 + y), 16, 16))
				full.append(f)
			self.panel_border.append(borders)
			self.panel_full.append(full)

	def draw_panel_full(self, width, height):
		return self.draw_panel(width, height, self.panel_full)
	def draw_panel_border(self, width, height):
		return self.draw_panel(width, height, self.panel_border)
	def draw_panel(self, width, height, sprites):
		surface = pygame.Surface((width, height), pygame.SRCALPHA)
		#corners
		surface.blit(sprites[0][0], (0, 0))
		surface.blit(sprites[2][0], (width - 16, 0))
		surface.blit(sprites[0][2], (0, height - 16))
		surface.blit(sprites[2][2], (width - 16, height - 16))
		#borders
		surface.blit(pygame.transform.scale(sprites[1][0], (width - 32, 16)), (16, 0))
		surface.blit(pygame.transform.scale(sprites[1][2], (width - 32, 16)), (16, height - 16))
		surface.blit(pygame.transform.scale(sprites[0][1], (16, height - 32)), (0, 16))
		surface.blit(pygame.transform.scale(sprites[2][1], (16, height - 32)), (width - 16, 16))
		#middle
		surface.blit(pygame.transform.scale(sprites[1][1], (width - 32, height - 32)), (16, 16))
		return surface
