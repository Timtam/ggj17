import pygame

from commons import *
from controls import *

class Credits:
    def __init__(self, screen):
        self.screen = screen
        self.channel = play_sound_bgm('assets/sound/bgm/credits.ogg')
        self.font = pygame.font.Font('assets/font/KenPixel Nova.ttf', 25)
        self.controls = []
        self.controls.append(ButtonControl(self.screen.get_width() - (self.screen.get_width() - 20), 20, 'Back to Menu', self.back_to_menu_clicked))

    def back_to_menu_clicked(self):
        get_common().get_main().change_view('MainMenu')

    def render(self):
        self.screen.fill((0,0,0))

        lable = self.font.render("---CREDITS---",1,(255,255,255))#zahlenwerte rgb
        self.screen.blit(lable,((self.screen.get_width()/2-50),self.screen.get_height()*0.06))#x,y position

        #BALANCE-BEGIN
        lable = self.font.render("---GAME PERFORMANCE---",1,(255,255,255))#zahlenwerte rgb
        self.screen.blit(lable,(self.screen.get_width()*0.111,self.screen.get_height()*0.15))#x,y position

        lable = self.font.render("Luise Rixrath",1,(255,255,255))#zahlenwerte rgb
        self.screen.blit(lable,(self.screen.get_width()*0.154,self.screen.get_height()*0.2))#x,y position

        lable = self.font.render("Henry Radke",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.155,self.screen.get_height()*0.25))#x,y position

        lable = self.font.render("Moritz Bloch",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.154,self.screen.get_height()*0.3))#x,y position

        #STORY-END

        #SOUND-BEGIN
        lable = self.font.render("---SOUND---",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.151,self.screen.get_height()*0.45))

        lable = self.font.render("Toni Barth",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.156,self.screen.get_height()*0.55))

        lable = self.font.render("Max Haarbach",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.149,self.screen.get_height()*0.5))
        #SOUND-END


        #PROGRAMMER-BEGIN
        lable = self.font.render("---PROGRAMMER---",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.73,self.screen.get_height()*0.15))

        lable = self.font.render("Erik Tauchert",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.75,self.screen.get_height()*0.2))

        lable = self.font.render("Christian Arp",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.7528,self.screen.get_height()*0.25))

        lable = self.font.render("Toni Barth",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.761,self.screen.get_height()*0.3))

        lable = self.font.render("Moritz Bloch",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.753,self.screen.get_height()*0.35))#x,y position
        #PROGRAMMER-END

        #ART-BEGIN
        lable = self.font.render("---ART---",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.7585,self.screen.get_height()*0.45))

        lable = self.font.render("David Siering",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.7525,self.screen.get_height()*0.5))

        lable = self.font.render("Henry Radke",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.7531,self.screen.get_height()*0.55))#x,y position
        #ART-ENDE

        #Licenses-Begin
        lable = self.font.render("---LICENSES---",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.453,self.screen.get_height()*0.65))


        lable = self.font.render("Kevin McLeod: http://www.incompetech.com",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.366,self.screen.get_height()*0.7))

        lable = self.font.render("TeknoAXE: http://teknoaxe.com/Home.php",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.369,self.screen.get_height()*0.75))

        lable = self.font.render("bass (free for non-commercial use)",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.387,self.screen.get_height()*0.8))

        lable = self.font.render("Kenney Game Assets (CC0)",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.424,self.screen.get_height()*0.85))

        lable = self.font.render("py2exe (MIT),  Pygame (LGPL v3),  Python (PSF)",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.365,self.screen.get_height()*0.9))

        lable = self.font.render("Hochschule Anhalt",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.115,self.screen.get_height()*0.955))

        lable = self.font.render("Prof. Dr. Schlechtweg-Dorendorf",1,(255,255,255))
        self.screen.blit(lable,(self.screen.get_width()*0.734,self.screen.get_height()*0.955))


        #Licenses-END

        #pics-Begin
        self.screen.blit(pygame.transform.scale(get_common().get_image("assets/level/enemies/skeleton_left.png"), (200, 200)),(self.screen.get_width()*0.75,self.screen.get_height()*0.65))

        self.screen.blit(pygame.transform.scale(get_common().get_image("assets/level/towers/watertower.png"), (120, 220)),(self.screen.get_width()*0.13,self.screen.get_height()*0.65))

        self.screen.blit(pygame.transform.scale(get_common().get_image("assets/credits/ggj_pix.png"), (450, 250)),(self.screen.get_width()*0.335,self.screen.get_height()*0.199))

        #pics-end

        for control in self.controls:
            control.draw(self.screen)

        pygame.display.flip()

    def update(self):
        for control in self.controls:
            control.update()

    def leave(self):
        self.channel.Stop()

    def handle_ev(self, event):
        pass
