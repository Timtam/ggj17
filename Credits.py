import pygame 
import sys
from commons import *
class Credits:
	def __init__(self):
		self.x = 1280
		self.y = 720
		
		pygame.init()
		self.screen = pygame.display.set_mode((self.x,self.y))
		self.font = pygame.font.Font('assets/font/KenPixel Nova.ttf', 25)
		
	def loop(self):
	
	
		while True:
			self.screen.fill((0,0,0))
			
			lable = self.font.render("---CREDITS---",1,(255,255,255))#zahlenwerte rgb
			self.screen.blit(lable,((self.x/2-50),self.y*0.06))#x,y position
			
			#BALANCE-BEGIN
			lable = self.font.render("---GAME PERFORMANCE---",1,(255,255,255))#zahlenwerte rgb
			self.screen.blit(lable,(self.x*0.111,self.y*0.15))#x,y position
			
			lable = self.font.render("Luise Rixrath",1,(255,255,255))#zahlenwerte rgb
			self.screen.blit(lable,(self.x*0.154,self.y*0.2))#x,y position
			
			lable = self.font.render("Henry Radke",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.155,self.y*0.25))#x,y position
			
			lable = self.font.render("Moritz Bloch",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.154,self.y*0.3))#x,y position
			
			#STORY-END
			
			#SOUND-BEGIN
			lable = self.font.render("---SOUND---",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.151,self.y*0.45))
			
			lable = self.font.render("Toni Barth",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.156,self.y*0.55))
			
			lable = self.font.render("Max Haarbach",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.149,self.y*0.5))
			#SOUND-END
		
			
			#PROGRAMMER-BEGIN
			lable = self.font.render("---PROGRAMMER---",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.73,self.y*0.15))
			
			lable = self.font.render("Erik Tauchert",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.75,self.y*0.2))
			
			lable = self.font.render("Christian Arp",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.7528,self.y*0.25))
			
			lable = self.font.render("Toni Barth",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.761,self.y*0.3))
			
			lable = self.font.render("Moritz Bloch",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.753,self.y*0.35))#x,y position
			#PROGRAMMER-END
			
			#ART-BEGIN
			lable = self.font.render("---ART---",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.7585,self.y*0.45))
			
			lable = self.font.render("David Siering",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.7525,self.y*0.5))
			
			lable = self.font.render("Henry Radke",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.7531,self.y*0.55))#x,y position
			#ART-ENDE
			
			#Licenses-Begin
			lable = self.font.render("---LICENSES---",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.453,self.y*0.65))
			
			
			lable = self.font.render("Kevin McLeod: http://www.incompetech.com",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.366,self.y*0.7))
			
			lable = self.font.render("TeknoAXE: http://teknoaxe.com/Home.php",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.369,self.y*0.75))
				
			lable = self.font.render("bass (free for non-commercial use)",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.387,self.y*0.8))
			
			lable = self.font.render("Kenney Game Assets (CC0)",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.424,self.y*0.85))
			
			lable = self.font.render("py2exe (MIT),  Pygame (LGPL v3),  Python (PSF)",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.365,self.y*0.9))
			
			lable = self.font.render("Hochschule Anhalt",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.115,self.y*0.955))
			
			lable = self.font.render("Prof. Dr. Schlechtweg-Dorendorf",1,(255,255,255))
			self.screen.blit(lable,(self.x*0.734,self.y*0.955))
			
			
			#Licenses-END
			
			#pics-Begin
			self.screen.blit(pygame.transform.scale(get_common().get_image("assets\level\enemies\skeleton_left.png"), (200, 200)),(self.x*0.75,self.y*0.65))
			
			self.screen.blit(pygame.transform.scale(get_common().get_image("assets/level/towers/watertower.png"), (120, 220)),(self.x*0.13,self.y*0.65))
			
			self.screen.blit(pygame.transform.scale(get_common().get_image("assets/credits/ggj_pix.png"), (450, 250)),(self.x*0.335,self.y*0.199))
			
			#pics-end
			
			pygame.display.flip()
			
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
					
		
	def leave(self):
		self.channel.Stop()

	def new_game_clicked(self):
		get_common().get_main().change_view('Level')

	def options_clicked(self):
		get_common().get_main().change_view('OptionsScreen')

	def exit_clicked(self):
		get_common().get_main().stop()

	def handle_ev(self, event):
		pass

	def update(self):
		for control in self.controls:
			control.update()

	def render(self):
		for control in self.controls:
			control.draw(self.screen)